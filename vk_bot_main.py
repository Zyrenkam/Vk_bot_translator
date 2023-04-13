import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from deep_translator import MyMemoryTranslator
from emoji_translate.emoji_translate import Translator

languages = {
    'африканский': 'af', 'албанский': 'sq', 'арабский': 'ar', 'армянский': 'hy',
    'азербайджанский': 'az', 'белорусский': 'be', 'бенгальский': 'bn', 'боснийский': 'bs',
    'китайский': 'zh-TW', 'чешский': 'cs', 'датский': 'da', 'голландский': 'nl', 'английский': 'en',
    'эстонский': 'et', 'филиппинский': 'tl', 'финский': 'fi', 'французский': 'fr',
    'немецкий': 'de', 'греческий': 'el', 'хинди': 'hi', 'исландский': 'is',
    'индонезийский': 'id', 'ирландский': 'ga', 'итальянский': 'it', 'японский': 'ja',
    'канадский': 'kn', 'казахский': 'kk', 'корейский': 'ko', 'латинский': 'la', 'латвийский': 'lv',
    'литовский': 'lt', 'люксембургский': 'lb', 'македонский': 'mk', 'монгольский': 'mn', 'норвежский': 'no',
    'персидский': 'fa', 'польский': 'pl', 'португальский': 'pt', 'русский': 'ru', 'сербский': 'sr',
    'словацкий': 'sk', 'словенский': 'sl', 'сомалийский': 'so', 'испанский': 'es', 'шведский': 'sv',
    'таджикский': 'tg', 'татарский': 'tt', 'турецкий': 'tr', 'туркменский': 'tk', 'украинский': 'uk',
    'узбекский': 'uz', 'вьетнамский': 'vi', 'валлийский': 'cy', 'йоруба': 'yo', 'зулу': 'zu', 'эмодзи': 'am'}


def translating(from_tr_index, to_tr_index, text_to_translate):
    if (from_tr_index == 'эмодзи') ^ (to_tr_index == 'эмодзи'):
        emo = Translator(exact_match_only=False, randomize=True)

        if from_tr_index == 'эмодзи':
            text_emoji = emo.demojify(text_to_translate)
            translation = MyMemoryTranslator(source='en',
                                            target=languages.get(to_tr_index)).translate(text=text_emoji)
            return translation
        else:
            translation = MyMemoryTranslator(source=languages.get(from_tr_index),
                                            target='en').translate(text=text_to_translate)

            text_emoji = emo.emojify(translation)
            return text_emoji
    elif (from_tr_index in languages.keys()) and (to_tr_index in languages.keys()):
        translation = MyMemoryTranslator(source=languages.get(from_tr_index),
                                        target=languages.get(to_tr_index)).translate(text=text_to_translate)
        translation.translate(text_to_translate)
        return translation
    else:
        return 'Такой язык мне не известен, возможно скоро я его добавлю(нет) \n' \
               'Может тут даже ошибка есть'


def check_and_start(txt):
    mess = txt.split('/')
    if txt.count('/') == 1:
        translate_to_lang = mess[0].replace(' ', '')[1::]
        text_to_translate = mess[1]
        print(f'to_lang : {translate_to_lang}, text: {text_to_translate}')
        return translating('русский', translate_to_lang, text_to_translate)
    elif txt.count('/') == 2:
        translate_from_lang = mess[0].replace(' ', '')[1::]
        translate_to_lang = mess[1].replace(' ', '')
        text_to_translate = mess[2]
        print(f'from_lang : {translate_from_lang}, to_lang: {translate_to_lang}, text: {text_to_translate}')
        return translating(translate_from_lang, translate_to_lang, text_to_translate)
    else:
        return 'Где-то появилась ошибка'


token = 'token'

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, 210520236)


def sender(id, text):
    vk_session.method('messages.send', {'chat_id': id, 'message': text, 'random_id': 0})


def chat_sender(id, text):
    vk_session.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0})


for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.from_chat:
            id = event.chat_id
            user_id = event.object.message['from_id']
            msg = str(event.object.message['text'].lower())
            print(user_id, ': ', msg)
            try:
                dey = event.message.action['type']
                invite_id = event.message.action['member_id']
            except:
                dey = ''
                invite_id = -100

            if dey == 'chat_invite_user':
                sender(id, f'Привет, @id{invite_id}!, я переводчик, чтобы меня использовать сделай следующее:')
                sender(id, '! язык / то, что нужно перевести')
                sender(id, 'ИЛИ \n ! С какого языка / На какой / текст')

            if msg == 'помоги пж':
                sender(id, '! язык / то, что нужно перевести')
                sender(id, 'ИЛИ \n ! С какого языка / На какой / текст')

            if msg[0] == '!':
                print(msg)
                text = msg
                sender(id, check_and_start(text))
