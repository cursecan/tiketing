from telegram.ext import (
    Updater, CommandHandler, Filters, 
    ConversationHandler, MessageHandler, RegexHandler
)

import requests
from decouple import config

STATION, TGL, TRAIN, PASS, FINISH = range(5)

WEB_BASE = config('WEB_BASE')


def getdata(a):
    rson = dict()
    r = requests.get(WEB_BASE + '/bm/tb/{}/'.format(a), timeout=10)
    if r.status_code == requests.codes.ok:
        rson = r.json()
    return rson

def helpCommand(bot, update):
    a = getdata('help')
    update.message.reply_html(
        a.get('body', 'Maaf perintah yang dimasukan salah.')
    )

def startCommand(bot, update):
    a = getdata('start')
    update.message.reply_html(
        a.get('body', 'Maaf perintah yang dimasukan salah.')
    )
    
def howtoCommand(bot, update):
    a = getdata('howto')
    update.message.reply_html(
        a.get('body', 'Maaf perintah yang dimasukan salah.')
    )

def rulesCommand(bot, update):
    a = getdata('rules')
    update.message.reply_html(
        a.get('body', 'Maaf perintah yang dimasukan salah.')
    )

def aboutCommand(bot, update):
    a = getdata('about')
    update.message.reply_html(
        a.get('body', 'Maaf perintah yang dimasukan salah.')
    )

def booking(bot, update):
    update.message.reply_html(
        "Hi <strong>{}</strong>,\nSaya akan membantu mengawal pemesanan tiket Anda. Silahkan ikuti prosedur berikut.".format(
            update.message.from_user.first_name
        )
    )

    update.message.reply_html(
        '🚉 STASIUN ASAL & TUJUAN\n\nSilahkan pilih stasiun asal dan tujuan.\n<i>Format : [st.asal] / [st.tujuan]</i>'
    )

    return STATION


def station(bot, update, user_data):
    user_data['station'] = update.message.text.upper()

    update.message.reply_html(
        '✨ Berhasil..!\n\nStasiun Asal & Tujuan Anda:\n<strong>{}</strong>.\n\n🗓 TANGGAL BERANGKAT\n\nSilahkan pilih tanggal keberangkatanya.\n<i>Format : [dd/mm/yyyy]</i>'.format(
            user_data['station']
        )
    )
    return TGL


def depart_date(bot, update, user_data):
    user_data['depart_date'] = update.message.text.upper()
    update.message.reply_html(
        "Rencana keberangkatan Anda tanggal : <strong>{}</strong>\n\n🚂 KERETA & KELAS LAYANAN\n\nSilahkan masukan kode kereta dan kelas (EKS/BIS/ECO).\n<i>** Kode kereta dapat dilihat di App KAI Access / Website KAI.</i>\n\n<i>Format : [kode kereta] / [kelas]</i>".format(
            user_data['depart_date']
        )
    )
    return TRAIN

def invalid_date(bot, update):
    update.message.reply_html(
        "Tanggal inputan tidak sesuai, silahkan masukan kembali sesuai format.\n\n<i>[dd/mm/yyyy]</i>"
    )
    return TGL

def train(bot, update, user_data):
    user_data['train'] = update.message.text.upper()
    update.message.reply_html(
        "🚆 <strong>{}</strong>\n\n👥 PENUMPANG\n\nMasukan nama dan nomor identitas penumpang.\n<i>Format : [nama_lengkap] / [no.id]</i>".format(
            user_data['train']
        )
    )
    return PASS

def passenger(bot, update, user_data):
    user_data['passenger'] = update.message.text.upper()
    update.message.reply_html(
        "✨✨✨✨✨✨\nBerikut data pemesanan Anda: \n\nAsal & Tujuan : <strong>{}</strong>\nTanggal Berangkat : <strong>{}</strong>\nNo. Kereta : <strong>{}</strong>\nPenumpang : <strong>{}</strong>\n\nApakah Anda yakin? (y/n)".format(
            user_data['station'],
            user_data['depart_date'],
            user_data['train'],
            user_data['passenger']
        )
    )
    return FINISH

def finish(bot, update, user_data):
    if update.message.text.upper() == 'Y':
        update.message.reply_html(
            "Terimakasih, proses booking selesai."
        )
        bot.send_message('@wanotif', str(update.message.from_user.id) +'\n\n'+ '\n'.join([user_data[i] for i in user_data]))

    else :
        update.message.reply_html(
            'Proses booking telah dibatalkan.'
        )
    return ConversationHandler.END

def unfinish(bot, update):
    update.message.reply_html(
        "Mohon dikonfirmasi kembali, masukan Anda tidak sesuai. (y/n)?"
    )

    return FINISH

def cancel(bot, update):
    """Log Errors caused by Updates."""
    update.message.reply_html(
        "Pemesanan Anda telah di cancel."
    )
    return ConversationHandler.END


def error(bot, update):
    """Log Errors caused by Updates."""
    print('Error')


updater = Updater(config('KAI_TOKEN_REQUEST'))

dp = updater.dispatcher

conv_hd = ConversationHandler(
    entry_points=[CommandHandler('booking', booking)],
    states = {
        STATION: [MessageHandler(Filters.text, station, pass_user_data=True)],
        TGL: [
            RegexHandler('^\d{1,2}/\d{1,2}/\d{4}$', depart_date, pass_user_data=True),
            MessageHandler(Filters.text, invalid_date),
        ],
        TRAIN: [MessageHandler(Filters.text, train, pass_user_data=True)],
        PASS: [MessageHandler(Filters.text, passenger, pass_user_data=True)],
        FINISH: [
            RegexHandler('^(Y|y|N|n)$', finish, pass_user_data=True),
            MessageHandler(Filters.text, unfinish),
        ]
    },
    fallbacks = [CommandHandler('cancel', cancel)]
)


dp.add_handler(CommandHandler('help', helpCommand))
dp.add_handler(CommandHandler('start', startCommand))
dp.add_handler(CommandHandler('howto', howtoCommand))
dp.add_handler(CommandHandler('rules', rulesCommand))
dp.add_handler(CommandHandler('about', aboutCommand))
dp.add_handler(conv_hd)
dp.add_error_handler(error)

updater.start_polling()
updater.idle()