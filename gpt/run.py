import os
import re
import time
from pathlib import Path

import jieba
import tensorflow as tf
from django.core.management.base import BaseCommand
from transformers import BertTokenizer
from transformers import GPT2Config
from transformers import TFGPT2LMHeadModel
from transformers.modeling_tf_utils import shape_list


class CustomAccuracy(tf.keras.metrics.SparseCategoricalAccuracy):

    def __init__(self, *args, tokenizer=None, **kwargs):
        self.tokenizer = tokenizer
        super(CustomAccuracy, self).__init__(*args, **kwargs)

    def update_state(self, labels, logits, sample_weight=None):
        active_loss = tf.not_equal(tf.reshape(labels, (-1,)), self.tokenizer.pad_token_id)
        reduced_logits = tf.boolean_mask(
            tf.reshape(logits, (-1, shape_list(logits)[2])), active_loss
        )
        labels = tf.boolean_mask(tf.reshape(labels, (-1,)), active_loss)
        return super().update_state(labels, reduced_logits, sample_weight)


def build_loss(tokenizer):
    def custom_loss(labels, logits):
        loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(
            from_logits=True, reduction=tf.keras.losses.Reduction.NONE
        )
        # make sure only labels that are not equal to -100 affect the loss
        active_loss = tf.not_equal(tf.reshape(labels, (-1,)), tokenizer.pad_token_id)
        reduced_logits = tf.boolean_mask(
            tf.reshape(logits, (-1, shape_list(logits)[2])), active_loss
        )
        labels = tf.boolean_mask(tf.reshape(labels, (-1,)), active_loss)
        return loss_fn(labels, reduced_logits)

    return custom_loss


def load_tokenizer():
    """ 获得 token """

    from transformers import BertTokenizer

    params = {
        'pretrained_model_name_or_path': "/Users/chenhaiou/Desktop/D/git/fund/gpt/tokenizer/",
        # 'pretrained_model_name_or_path': f"{settings.BASE_DIR}/gpt/tokenizer/",
        'max_len': 512,
    }
    try:
        tokenizer = BertTokenizer.from_pretrained(**params)
        # 修改 transformers/tokenization_utils_base.py line 1948
        # if added_tokens_file is not None:
        #     with open(added_tokens_file, encoding="utf-8") as added_tokens_handle:
        #         added_tok_encoder = json.load(added_tokens_handle)
        #     added_tok_encoder_sorted = list(sorted(added_tok_encoder.items(), key=lambda x: x[1]))
        #     tokens = [item[0] for item in added_tok_encoder_sorted]
        #     tokenizer.add_tokens(tokens)

    except EnvironmentError:
        params['pretrained_model_name_or_path'] = 'bert-base-chinese'
        tokenizer = BertTokenizer.from_pretrained(**params)
        tokenizer.return_attention_mask = None
        tokenizer.eos_token = tokenizer.sep_token
        tokenizer.save_pretrained('tokenizer')

    return tokenizer


def init_model(
        tokenizer: BertTokenizer,
) -> TFGPT2LMHeadModel:
    try:
        dirname = os.path.dirname(__file__)
        model_path = f'{dirname}/train_v1'
        model = TFGPT2LMHeadModel.from_pretrained(model_path)
    except EnvironmentError:
        config = GPT2Config(  # noqa
            architectures=["TFGPT2LMHeadModel"],
            model_type="TFGPT2LMHeadModel",
            tokenizer_class="XLNetTokenizer",
            vocab_size=tokenizer.vocab_size,
            n_positions=512,
            n_ctx=512,  # 指定上下文窗口的大小，即模型在预测下一个词时所考虑的前文的长度
            n_embd=768,
            n_layer=4,  # 指定模型的层数
            n_head=4,
            pad_token_id=tokenizer.pad_token_id,
            task_specific_params={
                "text-generation": {"do_sample": False, "max_length": 120}
            },
            return_dict=False,
            output_attentions=False,
            output_hidden_states=False,
            use_cache=False,
        )
        model = TFGPT2LMHeadModel(config)
    # model.resize_token_embeddings(len(tokenizer))
    loss = build_loss(tokenizer)
    optimizer = tf.keras.optimizers.Adam(learning_rate=5e-5, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
    metric = CustomAccuracy("accuracy", tokenizer=tokenizer)
    model.compile(
        optimizer=optimizer,
        loss=[loss, *[None] * model.config.n_layer],
        metrics=[metric],
    )
    return model


class Command(BaseCommand):
    @classmethod
    def cut_words(cls):
        """ 结巴分词，并将分词后的词加入 token """

        new_tokens = set()
        # 每句话提问和回答都加入[rep]作为区分。在预判输出时，如果不是[rep]开头的句子，不输出
        # new_tokens.add('[rep]')
        tokenizer = load_tokenizer()
        # 注册 lambda
        lambda_keys = set()
        file_paths = Path("/Users/chenhaiou/Desktop/D/git/fund/gpt/texts/").glob("*.txt")
        for file_path in file_paths:
            with open(file_path, 'r') as f:
                while line := f.readline():
                    line = line.strip()
                    if not line:
                        continue
                    if '[LAMBDA' in line:
                        lambda_key = line.split('[LAMBDA')[-1].split(']')[0]
                        lambda_key = f'[LAMBDA{lambda_key}]'
                        lambda_keys.add(lambda_key)
                    jieba_cut = jieba.lcut(line)
                    # 添加分词后的 token
                    new_tokens = new_tokens | set(jieba_cut)

        tokenizer.add_tokens(new_tokens=list(new_tokens))  # todo chenhaiou
        # tokenizer.add_tokens(new_tokens=list(lambda_keys))
        # tokenizer.add_tokens(new_tokens=['给我集团企业的', '给我登录运营公司', '给我登录企业客户', '帮我清空', '实名认证次数', '登录运营公司', "[rep]", ])
        # tokenizer.add_tokens(new_tokens=['：user-UserPlatform-', 'user-UserPlatform-', 'UserPlatform-', ])
        tokenizer.save_pretrained('tokenizer')
        return tokenizer

    @classmethod
    def get_dataset(cls, tokenizer):
        """ 拿到数据集 """

        import numpy as np
        import tensorflow as tf

        input_ids = []
        sample_size = 0
        max_len = 65
        file_paths = Path("/Users/chenhaiou/Desktop/D/git/fund/gpt/texts/").glob("*.txt")
        for file_path in file_paths:
            with open(file_path, 'r') as f:
                while line := f.readline():
                    line = line.strip().strip('\n')
                    if not line:
                        continue
                    line_decoded = tokenizer(line, )['input_ids']
                    if len(line_decoded) > max_len:
                        raise ValueError(f'训练文本长度 {len(line)} 超过{max_len - 2}: {line=}')
                    line_decoded = np.array(line_decoded, dtype=np.int32)
                    line_decoded = np.pad(line_decoded, (0, max_len - len(line_decoded)), 'constant', constant_values=(tokenizer.pad_token_id, tokenizer.pad_token_id))
                    input_ids.append(line_decoded)
                    sample_size += 1

        input_ids = np.array(input_ids)
        # 去掉最后一列，作为输入特征
        ids = input_ids[:, :-1]
        # 去掉第一列，作为标签
        labels = input_ids[:, 1:]
        dataset = (
            tf.data.Dataset.from_tensor_slices((ids, labels))
            .shuffle(ids.shape[0])
            # .repeat(20)
            # .batch(20)
            .repeat(40)
            .batch(20)
        )
        return dataset, sample_size

    def train(self, model, train_dataset, epochs: int, steps_per_epoch: int):

        import tensorflow as tf

        class AutoSaveCallback(tf.keras.callbacks.Callback):  # noqa

            def on_epoch_end(self, epoch, logs=None):  # noqa
                train_version = 'train_v1'
                self.model.save_pretrained(f"gpt/{train_version}")

        callbacks = [
            AutoSaveCallback(),
        ]

        t1 = time.time()
        # 修改 site-packages/transformers/modeling_tf_utils.py 中的 1665 改为 y_pred = y_pred[0]
        print(f'{model}')
        model.fit(
            train_dataset,
            epochs=epochs,
            steps_per_epoch=steps_per_epoch,
            callbacks=callbacks,
            batch_size=None,
        )
        print(f"total train time {time.time() - t1}")

    def train_main(self, tokenizer=None):

        import tensorflow as tf

        # epochs, steps_per_epoch = 1 * 10, 252 * 2
        epochs = 1 * 4
        mirrored_strategy = tf.distribute.MirroredStrategy()
        with mirrored_strategy.scope():
            if not tokenizer:
                tokenizer = load_tokenizer()
            train_dataset, sample_size = self.get_dataset(tokenizer)
            # steps_per_epoch = 样本数量 * repaet / batch_size
            steps_per_epoch = sample_size * 2
            model = init_model(tokenizer)
            self.train(model, train_dataset, epochs, steps_per_epoch)  # noqa

    @classmethod
    def predict(cls, tokenizer=None):
        """ 预判 """

        # from gpt.lambdas import LAMBDA_MAP
        from transformers import TextGenerationPipeline
        # from gpt.tokenizer import load_tokenizer

        print('predict', '.' * 120)
        if not tokenizer:
            tokenizer = load_tokenizer()
        model = init_model(tokenizer)

        # rep_token = tokenizer.get_vocab()['[rep]']
        text_generator = TextGenerationPipeline(model, tokenizer, return_tensors=True)
        text_inputs = {
            # '帮我查下关于"13520231413"的日志': {'testcase': 'lambda_sls'},
            '帮我清空身份证实名认证次数': {'testcase': 'lambda_clean_verify_labor_id_no'},
            # '给我登录企业客户"浙江壹米时空物流有限公司宁波分公司"的方式': {'testcase': 'lambda_company_login'},
            # '给我登录运营公司"浙江壹米时空物流有限公司宁波分公司"的方式': {'testcase': 'lambda_agency_login'},
            # '给我登录集团"浙江壹米时空物流有限公司宁波分公司"的方式': {'testcase': 'lambda_platform_login'},
            # '给我登录saas"浙江壹米时空物流有限公司宁波分公司"的方式': {'testcase': 'lambda_saas_login'},
            # '给我一个万能验证码': {'testcase': 'lambda_pyotp_sms_code'},
            # '提供下用户"UserAgency-921"的登录方式': {'testcase': 'lambda_get_user_by_id'},
            # '清空"371327198602012242"的实人认证次数': {'testcase': 'lambda_clean_auth_count'},
            # '请将用户"511304199609155015"的人脸识别次数清空': {'testcase': 'lambda_clean_auth_count'},
            # '匹配一下骑手系统号码': {'testcase': 'lambda_get_labor_mobile'},
            # '陶世伟 51102319890904987X 匹配下系统手机': {'testcase': 'lambda_get_labor_mobile'},
            # '文件用于匹配手机号': {'testcase': 'lambda_get_labor_mobile'},
            # '匹配一下系统手机号码': {'testcase': 'lambda_get_labor_mobile'},
            # "麻烦查一下：林新焕 440526197404263312，系统手机号码": {'testcase': 'lambda_get_labor_mobile'},
            # '匹配下系统手机号': {'testcase': 'lambda_get_labor_mobile'},
            # '请匹配这些身份证号在我们才得利系统关联的手机号码': {'testcase': 'lambda_get_labor_mobile'},
            # '给我集团企业的"13520230814"登录方式': {'testcase': 'lambda_platformcompany_login'},
            # '请放行实人认证': {'testcase': 'lambda_set_companylabor_in_cooperation'},
            # '放行实人认证': {'testcase': 'lambda_set_companylabor_in_cooperation'},
            # '最近天气怎么样': {'testcase': 'lambda_weather'},
            # '今天天气如何': {'testcase': 'lambda_weather'},
            # '天气怎么样': {'testcase': 'lambda_weather'},
            # '麻烦看一下 这个绑定银行次数 能不能重置一下': {'testcase': 'lambda_clean_identity3'},
            # '获得近期实人认证失败的视频': {'testcase': 'lambda_faceid_failed'},
            # '给我一份最新的卜丁租车的数据': {'testcase': 'lambda_bdinggo_data'},
            # '赵春红,请重置下人脸识别': {'testcase': 'lambda_clean_auth_count'},
        }

        for text_input in text_inputs:

            # 去掉变量，用 "" 包括起来的认为是变量
            text_input_short = text_input.replace('“', '"').replace('”', '"')
            text_input_short = text_input_short.split('"')[::2]
            text_input_short = ''.join(text_input_short)

            # 对话中是否存在疑似身份号码的文本
            match = re.search(r"\d{17}[\dXx]\b", text_input_short)
            if match:
                got_id_no = match.group()
                text_input_short = text_input_short.replace(got_id_no, '')

            generated_token_ids = text_generator(text_input_short, max_length=300, eos_token_id=tokenizer.eos_token_id)[0]['generated_token_ids']
            text_input_encode = tokenizer.encode(text_input_short, add_special_tokens=False)
            reply_token_ids = generated_token_ids[len(text_input_encode):]
            if reply_token_ids[-1] == tokenizer.sep_token_id:
                reply_token_ids = reply_token_ids[:-1]
            text_reply = tokenizer.decode(reply_token_ids)

            reply_encode = tokenizer.encode(text_reply, add_special_tokens=False)
            # if rep_token in reply_encode:
            #     reply_encode.remove(rep_token)
            #     text_reply = text_reply.replace('[rep]', '')

            # 触发函数
            # if '[LAMBDA' in text_reply:
            #     lambda_key = text_reply.split('[LAMBDA')[1]  # noqa
            #     lambda_key = lambda_key.split(']')[0]
            #     replace_text = f'[LAMBDA{lambda_key}]'
            #     if ':' in lambda_key:
            #         lambda_key_payload = lambda_key.split(':')[1]
            #         lambda_key_payload = lambda_key_payload.split(',')
            #     else:
            #         lambda_key_payload = []
            #     lambda_key = lambda_key.split(':')[0]
            #     lambda_key = f'[LAMBDA{lambda_key}]'
            #     text_reply = LAMBDA_MAP[lambda_key](
            #         text_input=text_input, text_reply=text_reply, replace_text=replace_text, lambda_key_payload=lambda_key_payload,
            #     )

            if 'testcase' in text_inputs[text_input]:
                if text_reply != text_inputs[text_input]['testcase']:
                    print(f"\033[91m✖️{text_input}:{text_reply}\033[0m")
                else:
                    print(f"\033[36m☑️{text_input}:{text_reply}\033[0m")


if __name__ == '__main__':
    # 结巴分词，并将词加入到 token 中
    self = Command()
    tokenizer = self.cut_words()
    # 训练模型
    self.train_main()
    # 预判
    self.predict(tokenizer)
    time.sleep(30)
