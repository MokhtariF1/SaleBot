ENV = 1
if ENV == 1:
    BOT_TOKEN = "7522711447:AAGa4p2Mqr_ebnmi6Wb95gvppGteYXdOD9I"
    API_ID = 28482138
    API_HASH = "cdcd9c0f111f85feaafac50d1bc3d6a5"
    PROXY = False
    PROXY_ADDRESS = ("socks5", "127.0.0.1", 2080)
    ADMINS = [5415792594, 100168441]
    CHANNEL_ID = "@taropood_textile"
    CHANNEL_LINK = "https://t.me/taropood_textile"
    BOT_ID = "Taropood_textile_bot"
else:
    BOT_TOKEN = "7920969267:AAGxT2VSBkjVyDo6_EfJY4m5cxpGDyH_QeQ"
    API_ID = 28482138
    API_HASH = "cdcd9c0f111f85feaafac50d1bc3d6a5"
    PROXY = False
    PROXY_ADDRESS = ("socks5", "127.0.0.1", 2080)
    ADMINS = [5415792594]
    CHANNEL_ID = "@hoooosseinbot"
    CHANNEL_LINK = "https://t.me/hoooosseinbot/"
    BOT_ID = "TestSaleRoBot"
buy_image = "./images/kharid.jpg"
sale_image = "./images/froosh.jpg"

bot_text = {
    "start": "کاربر عزیز به ربات خوش آمدید",
    "not_save_start": "کاربر عزیز، به ربات خوش آمدید💖\nبرای ادامه کار با ربات، ابتدا ثبت نام خود را کامل کنید✅",
    "info": "لطفا موارد زیر را تکمیل کنید. این اطلاعات در کارت ویزیت شما درج میشود و برای کسب و کار و بهبود ارتباط با شما مفید است",
    "rule": "آیا با قوانین زیر موافق هستید؟\nبعدا کامل میشود",
    "yes": "بله✅",
    "no": "خیر❌",
    "rule_not_conf": "برای ادامه و کار با ربات باید قوانین را تایید کنید❌",
    "select": "یک دکمه را انتخاب کنید:👇",
    "seller": "کسبه‌ی پارچه هستم (پارچه‌فروش ام)",
    "buyer": "مشتری خرید پارچه‌ام (پارچه‌فروش نیستم)",
    "enter_name": "نام کامل خود را وارد کنید:\nمثلا: حسین مختاری",
    "enter_business_name": "نام کسب و کار خود را وارد کنید: \n «مثلا: «مزون شیک پوش»  یا «قماش رضاپور",
    "enter_phone_number": "لطفا شماره همراه خود را وارد کنید: (ترجیحا واتس‌اپ و تلگرام داشته باشد)\nمثلا : ۰۹۳۵۱۲۳۴۵۶۷",
    "enter_business_phone": "شماره تلفن ثابت محل کار، برای ارتباط بهتر با شما (حتما با پیش‌شماره شهر وارد کنید) وارد کنید:",
    "enter_business_disc": "اگر مایلید، توضیحاتی در مورد کسب و کار خود وارد کنید (در کارت ویزیت شما درج میشود)\nمثلا : ارائه انواع پارچه‌های خارجی و ایرانی، کرپ‌جات، ژاکارد، مانتویی",
    "info_saved": "اطلاعات با موفقیت ذخیره شد✅\nمیتوانید کار خود را با ربات شروع کنید\n/start",
    "rule_conf": "قوانین با موفقیت تایید شد و حساب کاربری شما ساخته شد✅\nبرای تکمیل اطلاعات و شروع کار با ربات مجدد ربات را استارت کنید\n/start",
    "rule_before_conf": "قوانین قبلا تایید شده است!",
    "cancel": "کنسل کردن",
    "canceled": "درخواست شما کنسل شد",
    "share_phone": "اشتراک گذاری شماره✅",
    "error_phone": "خطا! لطفا مجدد مراحل را طی کرده و در مرحله شماره از طریق دکمه اشتراک گذاری شماره تلفن شماره خود را به اشتراک بگذارید\n/start",
    "share_phone_info": "کاربر عزیز، لطفا از طریق دکمه زیر شماره خود را با ربات به اشتراک بگذارید",
    "sale": "پیشنهاد فروش پارچه",
    "buy": "درخواست خرید پارچه",
    "enter_post_file": "تصویر اصلی پست خود را ارسال کنید",
    "has_image": "کاربر عزیز، آیا تصویری برای آگهی دارید؟",
    "error_media": "لطفا فقط تصویر یا ویدیو ارسال کنید! مجدد روی دکمه کلیک کنید و تلاش کنید",
    "enter_post_disc": "توضیحات آگهی را وارد کنید:\nبرای مثال نام پارچه و جزییات آن",
    "has_album": "آیا تصاویر دیگری برای آگهی دارید؟",
    "enter_album_image": "تصویر شماره {count} را وارد کنید",
    "has_another_image": "آیا تصویر دیگری دارید؟",
    "post_caption": """✨ <b>{title}</b> ✨

📝 <i>توضیحات</i>:
<blockquote><b>{caption}</b></blockquote>

🎯 <a href="https://t.me/taropood_textile">«تار و پود»  مرجع معرفی و خرید پارچه</a>""",
    "conf_btn": "✅ارسال آگهی به کانال",
    "post_not_found": "پست مورد نظر پیدا نشد❌",
    "sending_post_pre": "در حال ارسال پیش نمایش پست...",
    "sending_post": "در حال ارسال پست در کانال...",
    "post_sent": "پست با موفقیت در کانال ارسال شد✅",
    "show_more_images": "➕تصاویر بیشتر",
    "chat": "💬 چت پی‌وی",
    "cart": "👁‍🗨مشاهده کارت ویزیت",
    "how_many_price": "قیمت چند؟",
    "have_it": "موجود دارم",
    "error": "خطا!",
    "do_not_image": "این پست عکس های بیشتری ندارد!",
    "sending_images": "در حال ارسال تصاویر...",
    "cart_info": """
🔰🔰🔰🔰🔰   <b>کارت ویزیت</b>  🔰🔰🔰🔰🔰

✨   <b>{b_name}</b>   ✨

👤 {name}

📱 موبایل  {phone}
☎️  تلفن  {b_phone}

💫 {b_disc}

☑️  فعالیت:   {is_seller}

🎯 <a href="https://t.me/taropood_textile">«تار و پود»  مرجع معرفی و خرید پارچه</a>
""",
    "action_msg": '''پیام جدید از <b>{name}</b>، در مورد آگهی 
<blockquote><a href="{msg_link}"> {disc} </a></blockquote>,

 💬 متن پیام:
<b><blockquote>{text}</blockquote></b>
''',
    "action_sent": "پیام مورد نظر با موفقیت به کاربر ارسال شد\nمنتظر پاسخ کاربر باشید!",
    "cant_send_self": "شما نمیتوانید به خودتان پیام ارسال کنید!",
    "answer_msg": "✍🏻 پاسخ به پیام",
    "enter_answer": "کاربر عزیز، پاسخ خود را برای ارسال به کاربر وارد کنید:\nبرای کنسل کردن روی دکمه کنسل کلیک کنید",
    "user_not_found": "کاربر مورد نظر پیدا نشد!",
    "answer_text": '''پاسخ جدید از <b>{name}</b>، در مورد آگهی <blockquote><b><a href="{msg_link}"> {disc} </a> </b></blockquote>''',
    "answer_sent": "پیام شما با موفقیت به کاربر ارسال شد✅",
    "delete_post": "❌حذف آگهی",
    "suc_del": "پست با موفقیت حذف شد✅",
    "conf_post": "تایید آگهی✅",
    "post_notif": 'ادمین عزیز، پست جدیدی در کانال منتشر شده است\n<a href="{post_link}"> مشاهده پست </a>',
    "access_d": "دسترسی غیر مجاز!",
    "conf_post_suc": "پست با موفقیت تایید شد✅",
    "before_conf": "این پست از قبل تایید شده است!",
    "error_chat_media": "ارسال هرگونه عکس، ویدیو، فایل در چت مجاز نیست!",
    "you_msg": "شما : <b>{text}</b>",
    "msg": """
    {sender} : <b>{text}</b>
""",
}
