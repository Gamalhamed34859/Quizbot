from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import os

# توكن البوت
TOKEN = os.getenv("TELEGRAM_TOKEN", "7242992984:AAFQNFuTxXWSOyqMcazSXzKBk7Hyl6lDgno")

# إعدادات الإيميل
EMAIL_ADDRESS = "jamal.h.mohamed14@gmail.com"
EMAIL_PASSWORD = "unmo fsit tmvy prqa"
ADMIN_EMAIL = "gamalhamed482000@gmail.com"

# بيانات الطلاب (53 طالب)
students = {
    "1": "Mansour",
    "2": "Ali",
    "3": "Mohamed Yasser",
    "4": "Shrouk",
    "5": "Yehia",
    "6": "Omar",
    "7": "Raghad",
    "8": "Youssef",
    "9": "Abdulhamid",
    "10": "Yasser",
    "11": "Haifaa",
    "12": "Hanaa",
    "13": "Aseem",
    "14": "Khalid",
    "15": "Atheel",
    "16": "Yara",
    "17": "Razan",
    "18": "Mohamed_g",
    "19": "Zaid",
    "20": "Batool",
    "21": "Saeed GR 7",
    "22": "Ahmed",
    "23": "Sara",
    "24": "Khadija",
    "25": "Kareem",
    "26": "Mohamed Taher",
    "27": "Radwa",
    "28": "Malek",
    "29": "Farida",
    "30": "Mounira",
    "31": "Atef",
    "32": "Mohamed aboubakr",
    "33": "Mohamed Osman",
    "34": "Mostafa",
    "35": "Zein",
    "36": "Maryam",
    "37": "Salma",
    "38": "Nour",
    "39": "Doaa",
    "40": "Fares",
    "41": "Neo",
    "42": "Reem",
    "43": "Taghreed",
    "44": "Radwan",
    "45": "Yasmeen",
    "46": "Doaa",
    "47": "Faisal",
    "48": "Fatma",
    "49": "Mazen",
    "50": "Abd el Aziz",
    "51": "Lamees",
    "52": "Ibrahim",
    "53": "Bandar"
}

# الأسئلة (30 سؤال مع حقل image)
questions = [
    # رياضيات (10 أسئلة)
    {
        "text": "answer the question؟",
        "image": "https://pasteboard.co/qS0v1IFGtnmh.png",
        "options": ["12", "10", "8", "20"],
        "correct": 3
    },
    {
        "text": "answer the question",
        "image": "https://pasteboard.co/ezNt8oXb3j9r.png",
        "options": ["20", "35", "40", "66"],
        "correct": 2
    },
    {
        "text": "إذا كان x = 2، فما هو ناتج 3x + 1؟",
        "image": "https://pasteboard.co/BNK4YVMJRuvC.png",
        "options": ["6+ن", "7+ن", "ن+4", "0"],
        "correct": 3
    },
    {
        "text": "",
        "image": "https://pasteboard.co/a6RjymWaT023.png",
        "options": ["اخضر", "احمر", "اسود", "اصفر"],
        "correct": 3
    },
    {
        "text": "Easy Q",
        "image": "https://pasteboard.co/cYPdWkH4IB7I.png",
        "options": ["القيمه الاولي اكبر", "القيمه الثانيه", "متساويتان", "المعطيات غير كافيه"],
        "correct": 1
    },
    {
        "text": "",
        "image": "https://pasteboard.co/QZV0HNsWfitj.png",
        "options": ["2%", "30%", "40%", "20%"],
        "correct": 4
    },
    {
        "text": "",
        "image": "https://pasteboard.co/7mizOQULNv9x.png",
        "options": ["140", "60", "220", "100"],
        "correct": 3
    },
    {
        "text": " جاوب السؤال في ورقه خارجيه اذا ما قدرت تجاوبو ",
        "image": "https://pasteboard.co/hJjo9BJHgbCv.png",
        "options": ["تمام", "", "", ""],
        "correct": 1
    },
    {
        "text": "",
        "image": "https://pasteboard.co/BLqhV9jXkfaY.png",
        "options": ["14000 ريال", "12000ريال", "2ريال", "28000ريال"],
        "correct": 2
    },
    {
        "text": "",
        "image": "https://pasteboard.co/xGOfTKyKR9cu.png",
        "options": ["20", "40", "120", "10"],
        "correct": 4
    },
    # جغرافيا (10 أسئلة)
    {
        "text": "",
        "image": "https://pasteboard.co/uBoFxg8fvyfX.png",
        "options": ["38", "37", "36", "35"],
        "correct": 2
    },
    {
        "text": "",
        "image": "https://imgur.com/a/60IeDI6",
        "options": ["30", "35", "40", "مش عارف هجرب حظي"],
        "correct": 2
    },
    {
        "text": "؟",
        "image": "https://imgur.com/nn6uCEt",
        "options": ["20%", "40%", "60%", "25%"],
        "correct": 2
    },
    {
        "text": "",
        "image": "https://imgur.com/nA3Rhs5",
        "options": [" 1573 ", " 1234", "1577", "1576"],
        "correct": 1
    },
    {
        "text": "",
        "image": "https://imgur.com/t31su9K",
        "options": ["3", "6", "12", "5"],
        "correct": 3
    },
    {
        "text": " ",
        "image": "https://imgur.com/EWS2Zp6",
        "options": ["23", "26", "32", "44"],
        "correct": 2
    },
    {
        "text": " ",
        "image": "https://imgur.com/iWlzRbA",
        "options": ["4", "5", "6", "9"],
        "correct": 3
    },
    {
        "text": " ",
        "image": "https://imgur.com/1R2HKOC",
        "options": ["4000", "5000", "6000", "8000"],
        "correct": 1
    },
    {
        "text": "",
        "image": "https://imgur.com/j2Ya6fl",
        "options": ["القيمه الاولي", "القيمة الثانيه", "متساويتان", "ما ادري"],
        "correct": 2
    },
    {
        "text": "",
        "image": "https://imgur.com/PUgBQEc",
        "options": [" 12", "58 ", "13 ", " 10"],
        "correct": 2
    },
    # علوم (10 أسئلة)
    {
        "text": "",
        "image": "https://imgur.com/G4Hygw2",
        "options": ["10", "9000", "10000", "12000"],
        "correct": 3
    },
    {
        "text": "",
        "image": "https://imgur.com/PPGN471",
        "options": ["600", "300", "150", "200"],
        "correct": 1
    },
    {
        "text": "",
        "image": "https://imgur.com/eppcjk8",
        "options": ["القيمة الاولي اكبر", "القيمة الثانيه اكبر", "القيمتان متساويتان", "المعلومات غير كافيه"],
        "correct": 1
    },
    {
        "text": "",
        "image": "https://imgur.com/XawrN3k",
        "options": ["س + ص", "س² + ص ", "س²", " + 1"],
        "correct": 2
    },
    {
        "text": "",
        "image": "https://imgur.com/PlzK52W",
        "options": ["200", "230", "250", "370"],
        "correct": 2
    },
    {
        "text": "",
        "image": "https://imgur.com/QpSh6Ia",
        "options": ["10", "6", "12", "9"],
        "correct": 3
    },
    {
        "text": "",
        "image": "https://imgur.com/vn5kTOF",
        "options": ["57", "32", "16", "64"],
        "correct": 1
    },
    {
        "text": "",
        "image": "https://imgur.com/VJIs0X4",
        "options": ["12", "8", " 3 ", "5"],
        "correct": 2
    },
    {
        "text": "    ",
        "image": "https://imgur.com/pL6yKz9",
        "options": ["القيمة الاولي ", "القيمة الثانيه", "متساويتان", "المعلومات غير كافية"],
        "correct": 3
    },
    {
        "text": "",
        "image": "",
        "options": ["16", "17", "18", "19"],
        "correct": 2
    }
]

# تخزين حالة المستخدم
user_data = {}

# إعدادات التسجيل للتصحيح
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# دالة لاختبار اتصال الإيميل
def test_email_connection():
    try:
        logging.info("Testing email connection...")
        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=30)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.quit()
        logging.info("Email connection test successful!")
        return True
    except smtplib.SMTPAuthenticationError:
        logging.error("Authentication failed during test. Please check EMAIL_ADDRESS and EMAIL_PASSWORD (App Password required).")
        return False
    except Exception as e:
        logging.error(f"Email connection test failed: {str(e)}")
        return False

# دالة للتحقق من صيغة الإيميل
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# دالة لإرسال الإيميل
def send_email(to_email, student_name, score, total):
    try:
        logging.info(f"Attempting to send email to {to_email} and {ADMIN_EMAIL}")
        
        # إيميل للطالب
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg['Subject'] = "Your Aptitude Test Results Are In! 🎉"

        body = f"Hey {student_name},\n\n" \
               f"Congrats on completing the aptitude test! 🎉 Here’s how you did:\n\n" \
               f"Your Score:\n" \
               f"Total Score: {score}\n" \
               f"Correct Answers: {score}\n\n" \
               f"Now, don't get too comfortable just yet! We’ll be going over all the questions in detail on Tuesday at 3:00 PM, so make sure you’re there! 😎\n\n" \
               f"And trust me, don't even think about skipping it — no naps, no excuses! You’ll want to be awake for this one! 😆\n\n" \
               f"Catch you then,\n" \
               f"Mr.Jamal\n" \
               f"{EMAIL_ADDRESS}"
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        # إيميل للأدمن
        msg_admin = MIMEMultipart()
        msg_admin['From'] = EMAIL_ADDRESS
        msg_admin['To'] = ADMIN_EMAIL
        msg_admin['Subject'] = f"نتيجة الطالب {student_name}"
        body_admin = f"الطالب: {student_name}\n" \
                     f"النتيجة: {score}/{total}"
        msg_admin.attach(MIMEText(body_admin, 'plain', 'utf-8'))

        # الاتصال بخادم Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=30)
        server.starttls()
        logging.info("TLS started")
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        logging.info("Login successful")
        server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        server.sendmail(EMAIL_ADDRESS, ADMIN_EMAIL, msg_admin.as_string())
        server.quit()
        logging.info(f"Email successfully sent to {to_email} and {ADMIN_EMAIL}")
        return True
    except smtplib.SMTPAuthenticationError:
        logging.error("Authentication failed. Check if App Password is correct.")
        return False
    except smtplib.SMTPException as e:
        logging.error(f"SMTP error occurred: {str(e)}")
        return False
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    logging.info(f"User {user_id} started the bot")
    
    await update.message.reply_text(
        "أهلًا بك! 👋\n"
        "هذا بوت الاختبارات التعليمية.\n"
        "اكتب رقم الطالب الخاص بك للبدء."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()
    logging.info(f"User {user_id} sent: {text}")

    if user_id not in user_data:
        if text in students:
            # التحقق إذا كان الطالب رقم 12 أو 25
            if text in ["12", "25"]:
                user_data[user_id] = {
                    "student_id": text,
                    "name": students[text],
                    "state": "waiting_for_quiz",
                    "score": 0,
                    "current_question": 0
                }
                await update.message.reply_text(
                    f"مرحبًا {students[text]}! 👋\n"
                    "اكتب /start_quiz لبدء الاختبار."
                )
            else:
                await update.message.reply_text(
                    f"يا {students[text]}، انت معندكش اختبار دلوقتي المفروض وكلمني لو فيه مشكله بتقابلك"
                )
        else:
            await update.message.reply_text("⚠️ رقم الطالب غير صحيح. حاول مرة أخرى.")
    
    elif user_data[user_id]["state"] == "in_quiz":
        try:
            answer = int(text)
            current_q = user_data[user_id]["current_question"]
            
            if 1 <= answer <= 4:
                if answer == questions[current_q]["correct"]:
                    user_data[user_id]["score"] += 1
                    await update.message.reply_text("✅ إجابة صحيحة!")
                else:
                    correct_answer = questions[current_q]["options"][questions[current_q]["correct"]-1]
                    await update.message.reply_text(f"❌ إجابة خاطئة! الإجابة الصحيحة هي: {correct_answer}")
                
                user_data[user_id]["current_question"] += 1
                await send_question(update, context)
            else:
                await update.message.reply_text("⚠️ الرجاء إدخال رقم بين 1 و 4.")
        
        except ValueError:
            await update.message.reply_text("⚠️ الرجاء إدخال رقم الإجابة فقط (1-4).")
    
    elif user_data[user_id]["state"] == "waiting_for_email":
        # التحقق من صيغة الإيميل
        if is_valid_email(text):
            user_data[user_id]["email"] = text
            score = user_data[user_id]["score"]
            total = len(questions)
            name = user_data[user_id]["name"]
            
            # إرسال الإيميل
            if send_email(text, name, score, total):
                await update.message.reply_text(
                    f"🏁 تم إرسال نتيجتك إلى {text}!\n"
                    f"شكرًا لك {name}!"
                )
            else:
                await update.message.reply_text(
                    "⚠️ حدث خطأ أثناء إرسال النتيجة. يرجى المحاولة لاحقًا أو التواصل مع المسؤول."
                )
            del user_data[user_id]
        else:
            await update.message.reply_text("⚠️ الرجاء إدخال بريد إلكتروني صحيح (مثال: name@example.com).")

async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    try:
        if user_data[user_id]["current_question"] < len(questions):
            current_q = user_data[user_id]["current_question"]
            question = questions[current_q]
            
            # تسجيل تفاصيل السؤال للتصحيح
            logging.info(f"Sending question {current_q + 1} to user {user_id}: {question['text']}, Image: {question['image']}")
            
            # إعداد نص السؤال
            caption = (
                f"السؤال {current_q + 1}: {question['text']}\n\n"
                f"1. {question['options'][0]}\n"
                f"2. {question['options'][1]}\n"
                f"3. {question['options'][2]}\n"
                f"4. {question['options'][3]}\n\n"
                "اكتب رقم الإجابة (1-4):"
            )
            
            # إذا كان فيه رابط صورة، ابعتها مع الصورة
            if question["image"]:
                await update.message.reply_photo(
                    photo=question["image"],
                    caption=caption
                )
            else:
                # لو مافيش صورة، ابعت تك Aerosol
                await update.message.reply_text(caption)
        
        else:
            # انتهاء الاختبار، طلب الإيميل
            user_data[user_id]["state"] = "waiting_for_email"
            await update.message.reply_text(
                "🏁 انتهى الاختبار!\n"
                "من فضلك، اكتب بريدك الإلكتروني لإرسال النتيجة (مثال: name@example.com):"
            )
    
    except Exception as e:
        logging.error(f"Error in send_question for user {user_id}, question {user_data[user_id]['current_question']}: {e}")
        await update.message.reply_text("⚠️ حدث خطأ في إرسال السؤال. يرجى المحاولة لاحقًا.")
        del user_data[user_id]

async def start_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    logging.info(f"User {user_id} started quiz")

    if user_id in user_data and user_data[user_id]["state"] == "waiting_for_quiz":
        user_data[user_id].update({
            "state": "in_quiz",
            "current_question": 0,
            "score": 0
        })
        await update.message.reply_text("بدأ الاختبار! 🚀")
        await send_question(update, context)
    else:
        await update.message.reply_text("⚠️ يرجى إدخال رقم الطالب أولًا.")

async def main():
    # اختبار اتصال الإيميل
    if not test_email_connection():
        logging.warning("Email connection test failed. Bot will run, but emails may not send.")
    
    # إنشاء التطبيق
    application = Application.builder().token(TOKEN).build()
    
    # إضافة معالجات الأوامر
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("start_quiz", start_quiz))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # بدء البوت
    logging.info("Starting bot...")
    await application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())