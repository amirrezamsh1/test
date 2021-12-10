import telegram
from telegram import (ReplyKeyboardMarkup,InlineKeyboardMarkup,InlineKeyboardButton)
from telegram.ext import Updater
from telegram.ext import (CommandHandler,MessageHandler,CallbackQueryHandler,Filters)
import logging
import sqlite3
import pandas as pd
import datetime
import datetime as dt

updater=Updater(token='2041358021:AAFIhdcxrIznPxpU6njaVW5LFdDs-0WiPhw',use_context=True)

dispatcher=updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)


conn=sqlite3.connect('varzesh.sqlite',check_same_thread=False)
cur=conn.cursor()
#cur.execute('''
#            CREATE TABLE IF NOT EXISTS Data(
#                id INTEGER PRIMARY KEY AUTOINCREMENT,
#                user_name TEXT NULL,
#                user_id TEXT UNIQUE NULL,
#                student_id INTEGER UNIQUE NULL,
#                level INTEGER NULL)''')


def start_function(update,context) :
    all_ids=cur.execute('SELECT user_id FROM Data')
    id=[i[0] for i in all_ids if i[0]!=None]
    if str(update.message.chat.id) in id :
        pass
    else :
        starttext="به ربات خوش آمدید، لطفا نام و نام خانوادگی خود را به صورت صحیح وارد کنید"
        context.bot.send_message(chat_id=update.effective_chat.id,text=starttext)
        cur.execute('INSERT INTO Data (user_id,level) VALUES (?,?)',(update.message.chat.id,0))
        conn.commit()
        #print('start done')


def text_function(update,context) :
    id=str(update.message.chat.id)
    cur.execute('SELECT level FROM Data WHERE user_id=?',(update.message.chat.id,))
    level=cur.fetchone()[0]
    print(level)
    if level==0 :
        name=update.message.text
        cur.execute('UPDATE Data SET user_name=? WHERE user_id=?',(name,update.message.chat.id))
        cur.execute('UPDATE Data SET level=1 WHERE user_id=?',(update.message.chat.id,))
        conn.commit()
        text="نام شما با موفقیت ثبت شد، لطفا شماره دانشجویی خود را وارد کنید"
        context.bot.send_message(chat_id=update.effective_chat.id,text=text)
    elif level==1 :
        id=update.message.text
        cur.execute('UPDATE Data SET student_id=? WHERE user_id=?',(id,update.message.chat.id))
        cur.execute('UPDATE Data SET level=2 WHERE user_id=?',(update.message.chat.id,))
        conn.commit()
        text="اطلاعات شما تکمیل شد و شما میتوانید از طریق منو تکالیف خود را آپلود نمایید"
        context.bot.send_message(chat_id=update.effective_chat.id,text=text)
    elif level==5 :
        subject=update.message.text
        cur.execute('UPDATE Data SET subject=? WHERE user_id=?',(subject,update.message.chat.id))
        conn.commit()
        df=pd.read_csv('presentation.csv')
        capacity=df['remain'].tolist()
        C=['('+str(i)+')' for i in capacity]
        keyboard=[[InlineKeyboardButton('1400/07/22 '+C[0],callback_data='07-22_'+id),InlineKeyboardButton('1400/07/29 '+C[1],callback_data='07-29_'+id)],
        [InlineKeyboardButton('1400/08/06 '+C[2],callback_data='08-06_'+id),InlineKeyboardButton('1400/08/13 '+C[3],callback_data='08-13_'+id)],
        [InlineKeyboardButton('1400/08/20 '+C[4],callback_data='08-20_'+id),InlineKeyboardButton('1400/08/27 '+C[5],callback_data='08-27_'+id)],
        [InlineKeyboardButton('1400/09/04 '+C[6],callback_data='09-04_'+id),InlineKeyboardButton('1400/09/11 '+C[7],callback_data='09-11_'+id)],
        [InlineKeyboardButton('1400/09/18 '+C[8],callback_data='09-18_'+id),InlineKeyboardButton('1400/09/25 '+C[9],callback_data='09-25_'+id)]]

        inline_markup=InlineKeyboardMarkup(keyboard)

        text='روز ارایه خود را از میان یکی از روز های زیر انتخاب کنید'
        context.bot.send_message(chat_id=update.effective_chat.id,text=text,reply_markup=inline_markup)

def assignment_1(update,context) :
    userid=update.message.chat.id
    cur.execute('SELECT assignment1 FROM Data WHERE user_id=?',(userid,))
    assignment=cur.fetchone()[0]
    if assignment==None :
        text="""
در این تکلیف به مواردی نظیر نام، نام خانوادگی، رشته تحصیلی، سن، قد، وزن، شاخص توده بدنی و سوابق ورزشی اشاره نمایید و در قالب یک فایل پی دی اف آپلود کنید
دقت کنید که فرمت فایل باید حتما به صورت پی دی اف باشد در غیر این صورت قابل قبول نیست"""
    #    cur.execute('UPDATE Data SET level=3 WHERE user_id=?',(update.message.chat.id,))
    #    conn.commit()

        keyboard=[[InlineKeyboardButton('ارسال تکلیف',callback_data='asg1_'+str(userid)+'.send'),
            InlineKeyboardButton('بعدا ارسال میکنم',callback_data='asg1_'+str(userid)+'.cancel')]]

        inline_markup=InlineKeyboardMarkup(keyboard)

        context.bot.send_message(chat_id=update.effective_chat.id,text=text,reply_markup=inline_markup)
    else :
        text="شما این تکلیف را تحویل داده اید"
        context.bot.send_message(chat_id=update.effective_chat.id,text=text)

def button(update,context) :
    query = update.callback_query
    query.answer()
    userid=query.data.split('_')[1].split('.')[0]
    if '1' in (query.data).split('_')[0] :
        if (query.data).endswith('send') :
            text='فایل پی دی اف این تکلیف را ارسال کنید'
            cur.execute('UPDATE Data SET level=3 WHERE user_id=?',(userid,))
            conn.commit()

        else :
            text='باشه'
        query.edit_message_text(text=text)
    elif '3' in (query.data).split('_')[0] :
        if (query.data).endswith('send') :
            text='فایل زیپ این تکلیف را ارسال کنید'
            cur.execute('UPDATE Data SET level=7 WHERE user_id=?',(userid,))
            conn.commit()
        else :
            text='باشه'
        query.edit_message_text(text=text)
    elif '2' in (query.data).split('_')[0] :
        if (query.data).endswith('send') :
            text="فایل پی دی اف و تایپ شده این تکلیف را ارسال کنید"
            cur.execute('UPDATE Data SET level=9 WHERE user_id=?',(userid,))
            conn.commit()
        else :
            text="باشه"
        query.edit_message_text(text=text)

def title(prefix,format) :
    t=str(dt.datetime.now())
    a1=t.split()[0].replace('-','')
    a2=t.split()[1].split('.')[0].replace(':','')
    return prefix+'_'+a1+a2+'.'+format


def pdf_function(update,context) :
    cur.execute('SELECT level FROM Data WHERE user_id=?',(update.message.chat.id,))
    level=cur.fetchone()[0]
    if level==3 :
        pdf_id=update.message.document.file_id
        pdf_file=context.bot.get_file(pdf_id)
        filename=title('asg1','pdf')
        pdf_file.download('asg1//'+filename)
        cur.execute('UPDATE Data SET assignment1=? WHERE user_id=?',(filename,update.message.chat.id))
        cur.execute('UPDATE Data SET level=4 WHERE user_id=?',(update.message.chat.id,))
        conn.commit()
        text='تکلیف با موفقیت دریافت شد'
        context.bot.send_message(chat_id=update.effective_chat.id,text=text)
    elif level==9 :
        pdf_id=update.message.document.file_id
        pdf_file=context.bot.get_file(pdf_id)
        filename=title('asg2','pdf')
        pdf_file.download('asg2//'+filename)
        cur.execute('UPDATE Data SET assignment2=? WHERE user_id=?',(filename,update.message.chat.id))
        cur.execute('UPDATE Data SET level=10 WHERE user_id=?',(update.message.chat.id,))
        conn.commit()
        text='تکلیف با موفقیت دریافت شد'
        context.bot.send_message(chat_id=update.effective_chat.id,text=text)

def presentation(update,context) :
    cur.execute('SELECT subject FROM Data WHERE user_id=?',(update.message.chat.id,))
    subject=cur.fetchone()[0]
    if subject==None :
        cur.execute('UPDATE Data SET level=5 WHERE user_id=?',(update.message.chat.id,))
        conn.commit()
        subjects=cur.execute('SELECT subject FROM Data')
        s=[i[0] for i in subjects if i[0]!=None]
        if len(s)==0 :
            text='موضوع ارایه خود را وارد کنید'
        else :
            reserved_s='/'.join(s)
            reserved_s='\n'+reserved_s
            text="موضوع ارایه خود را وارد کنید و سعی کنید موضوعتان تکراری نباشد. موضوع های ارایه شده تاکنون به صورت زیر میباشد."+reserved_s
    else :
        text='شما موضوع خود را انتخاب کرده اید و امکان تغییر آن نیست'
    context.bot.send_message(chat_id=update.effective_chat.id,text=text)

def date_function(update,context) :
    query = update.callback_query
    query.answer()
    userid=(query.data).split('_')[1]
    date=(query.data).split('_')[0]

    df=pd.read_csv('presentation.csv')
    remain=df[df['date']==date]['remain'].tolist()[0]
    if remain>0 :
        index=df[df['date']==date].index.tolist()[0]
        df.loc[index,'remain']=remain-1
        df.to_csv('presentation.csv',index=False)
        cur.execute('UPDATE Data SET date=? WHERE user_id=?',(date,userid))
        cur.execute('UPDATE Data SET level=6 WHERE user_id=?',(userid,))
        conn.commit()
        cur.execute('SELECT subject FROM Data WHERE user_id=?',(userid,))
        subject=cur.fetchone()[0]
        information='\n'.join([subject,date])
        text='با موفقیت ثبت شد، موضوع و تاریخ ارایه شما به صورت زیر است'+'\n'+information
        query.edit_message_text(text=text)

    else :
        text='ظرفیت در تاریخ مورد نظر تکمیل است'


        capacity=df['remain'].tolist()
        C=['('+str(i)+')' for i in capacity]


        keyboard=[[InlineKeyboardButton('1400/07/22 '+C[0],callback_data='07-22_'+userid),InlineKeyboardButton('1400/07/29 '+C[1],callback_data='07-29_'+userid)],
        [InlineKeyboardButton('1400/08/06 '+C[2],callback_data='08-06_'+userid),InlineKeyboardButton('1400/08/13 '+C[3],callback_data='08-13_'+userid)],
        [InlineKeyboardButton('1400/08/20 '+C[4],callback_data='08-20_'+userid),InlineKeyboardButton('1400/08/27 '+C[5],callback_data='08-27_'+userid)],
        [InlineKeyboardButton('1400/09/04 '+C[6],callback_data='09-04_'+userid),InlineKeyboardButton('1400/09/11 '+C[7],callback_data='09-11_'+userid)],
        [InlineKeyboardButton('1400/09/18 '+C[8],callback_data='09-18_'+userid),InlineKeyboardButton('1400/09/25 '+C[9],callback_data='09-25_'+userid)]]


        inline_markup=InlineKeyboardMarkup(keyboard)

        query.edit_message_text(text=text)
        context.bot.send_message(chat_id=update.effective_chat.id,text='روز دیگری را انتخاب نمایید',reply_markup=inline_markup)

def present_files(update,context) :
    userid=str(update.message.chat.id)
    cur.execute('SELECT assignment3 FROM Data WHERE user_id=?',(userid,))
    assignment=cur.fetchone()[0]
    if assignment==None :
        text="تمام فایل های مربوط به ارایه را در یک فایل زیپ ذخیره کنید و آن را ارسال کنید، دقت کنید فایل ارسالی حتما باید به صورت زیپ باشد در غیر این صورت بات آن را دریافت نمیکند"
        keyboard=[[InlineKeyboardButton('ارسال تکلیف',callback_data='asg3_'+userid+'.send'),InlineKeyboardButton('بعدا ارسال میکنم',callback_data='asg3_'+userid+'.cancel')]]
        inline_markup=InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=int(userid),text=text,reply_markup=inline_markup)
    else :
        text="شما این تکلیف را ارسال کرده اید و امکان تغییر آن نیست"
        context.bot.send_message(chat_id=int(userid),text=text)

def zip_function(update,context) :
    cur.execute('SELECT level FROM Data WHERE user_id=?',(str(update.message.chat.id),))
    level=cur.fetchone()[0]
    if level==7 :
        zip_id=update.message.document.file_id
        zip_file=context.bot.get_file(zip_id)
        filename=title('asg3','zip')
        #filename='asg3_'+str(dt.datetime.now()).split('.')[1]+'.zip'
        zip_file.download('asg3//'+filename)
        cur.execute('UPDATE Data SET assignment3=? WHERE user_id=?',(filename,str(update.message.chat.id)))
        cur.execute('UPDATE Data SET level=8 WHERE user_id=?',(str(update.message.chat.id),))
        conn.commit()
        text='فایل ارایه با موفقیت دریافت شد'
        context.bot.send_message(chat_id=update.effective_chat.id,text=text)

def question_function(update,context) :
    userid=str(update.message.chat.id)
    cur.execute('SELECT assignment2 FROM Data WHERE user_id=?',(userid,))
    assignment=cur.fetchone()[0]
    if assignment==None :
        #text="تمام فایل های مربوط به ارایه را در یک فایل زیپ ذخیره کنید و آن را ارسال کنید، دقت کنید فایل ارسالی حتما باید به صورت زیپ باشد در غیر این صورت بات آن را دریافت نمیکند"
        text="چهار سوال تستی به همراه جواب به صورت تایپ شده از پی دی اف های داخل گروه طرح نمایید و در قالب فایل پی دی اف ارسال نمایید، دقت شود که فایل دست نویس قابل قبول نیست"
        keyboard=[[InlineKeyboardButton('ارسال تکلیف',callback_data='asg2_'+userid+'.send'),InlineKeyboardButton('بعدا ارسال میکنم',callback_data='asg2_'+userid+'.cancel')]]
        inline_markup=InlineKeyboardMarkup(keyboard)
        context.bot.send_message(chat_id=int(userid),text=text,reply_markup=inline_markup)
    else :
        text="شما این تکلیف را ارسال کرده اید و امکان تغییر آن نیست"
        context.bot.send_message(chat_id=int(userid),text=text)



start_handler=CommandHandler('start',start_function)
text_handler=MessageHandler(Filters.text & ~(Filters.command),text_function)
intro_handler=CommandHandler('intro',assignment_1)
callback_handler=CallbackQueryHandler(button)
pdf_handler=MessageHandler(Filters.document.mime_type("application/pdf"),pdf_function)
present_handler=CommandHandler('present',presentation)
presentdate_handler=CallbackQueryHandler(date_function,pattern='\d{2}-\d{2}.+')
presentf_handler=CommandHandler('prsntfile',present_files)
zip_handler=MessageHandler(Filters.document.mime_type("application/zip"),zip_function)
questions_handler=CommandHandler('questions',question_function)


dispatcher.add_handler(start_handler)
dispatcher.add_handler(text_handler)
dispatcher.add_handler(intro_handler)
dispatcher.add_handler(presentdate_handler)
dispatcher.add_handler(callback_handler)
dispatcher.add_handler(pdf_handler)
dispatcher.add_handler(present_handler)
dispatcher.add_handler(presentf_handler)
dispatcher.add_handler(zip_handler)
dispatcher.add_handler(questions_handler)



updater.start_polling()
