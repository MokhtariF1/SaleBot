import random
from telethon import TelegramClient, events,Button, types
import config
from pymongo import MongoClient
import mimetypes
from bson import ObjectId
import time

bot = TelegramClient("robot", config.API_ID, config.API_HASH,
                     proxy=None if config.PROXY is False else config.PROXY_ADDRESS)
print("connecting...")
bot.start(bot_token=config.BOT_TOKEN)
print("connected!")
bot_text = config.bot_text
bot.parse_mode = "html"
# connect to mongodb
connection = MongoClient("localhost", 27017)
db = connection["sale_bot"]
users_collection = db["users"]
post_collection = db["post"]
config_coll = db["config"]
msg_coll = db["msg"]
answers_coll = db["answers"]
main_buttons = [
    [
        Button.text(bot_text["buy"], resize=True),
        Button.text(bot_text["sale"])
    ]
]

@bot.on(events.NewMessage())
async def start(event):
    # print(event)
    user_id = event.sender_id
    find_user = users_collection.find_one({"user_id": user_id})
    text = event.message.message
    if text.startswith("/start"):
        if find_user is None:
            await event.reply(bot_text["not_save_start"])
            btns = [
                Button.inline(bot_text["yes"], b'rule_yes'),
                Button.inline(bot_text["no"], b'rule_no'),
            ]
            await event.reply(bot_text["rule"], buttons=btns)
        else:
            registered = find_user["registered"]
            if registered is False:
                async with bot.conversation(user_id, timeout=1000) as conv:
                    job_btn = [
                        [
                            Button.inline(bot_text["seller"], b'seller'),
                        ],
                        [
                            Button.inline(bot_text["buyer"], b'buyer')
                        ],
                    ]
                    cancel_btn = [Button.inline(bot_text["cancel"], b'cancel')]
                    job_btn.append(cancel_btn)
                    await conv.send_message(bot_text["select"], buttons=job_btn)
                    response1 = await conv.wait_event(events.CallbackQuery())
                    response = response1.data
                    is_seller = False
                    if response == b'cancel':
                        await response1.answer(bot_text["canceled"])
                        await response1.delete()
                        return
                    if response == b'seller':
                        is_seller = True
                        await response1.delete()
                    else:
                        await response1.delete()
                    text_cancel_btn = [Button.text(bot_text["cancel"], resize=True)]
                    phone_btns = [
                        [
                            Button.request_phone(bot_text["share_phone"], resize=True)
                        ],
                        text_cancel_btn
                    ]
                    await conv.send_message(bot_text["share_phone_info"], buttons=phone_btns)
                    phone = await conv.get_response()
                    if phone.raw_text == bot_text["cancel"]:
                        await conv.send_message(bot_text["canceled"], buttons=Button.clear())
                        return
                    phone = phone.media
                    if phone is None or type(phone) != types.MessageMediaContact:
                        await event.reply(bot_text["error_phone"])
                        return
                    phone = phone.phone_number
                    await conv.send_message(bot_text["enter_name"], buttons=text_cancel_btn)
                    name = await conv.get_response()
                    name = name.raw_text
                    if name == bot_text["cancel"]:
                        await conv.send_message(bot_text["canceled"], buttons=Button.clear())
                        return
                    await conv.send_message(bot_text["enter_business_name"], buttons=text_cancel_btn)
                    business_name = await conv.get_response()
                    business_name = business_name.raw_text
                    if business_name == bot_text["cancel"]:
                        await conv.send_message(bot_text["canceled"], buttons=Button.clear())
                        return
                    await conv.send_message(bot_text["enter_phone_number"], buttons=text_cancel_btn)
                    cart_phone = await conv.get_response()
                    cart_phone = cart_phone.raw_text
                    if cart_phone == bot_text["cancel"]:
                        await conv.send_message(bot_text["canceled"], buttons=Button.clear())
                        return
                    await conv.send_message(bot_text["enter_business_phone"], buttons=text_cancel_btn)
                    business_phone = await conv.get_response()
                    business_phone = business_phone.raw_text
                    if business_phone == bot_text["cancel"]:
                        await conv.send_message(bot_text["canceled"], buttons=Button.clear())
                        return
                    await conv.send_message(bot_text["enter_business_disc"], buttons=text_cancel_btn)
                    business_disc = await conv.get_response()
                    business_disc = business_disc.raw_text
                    if business_disc == bot_text["cancel"]:
                        await conv.send_message(bot_text["canceled"], buttons=Button.clear())
                        return
                    user = {
                        "is_seller": is_seller,
                        "name": name,
                        "business_name": business_name,
                        "phone": phone,
                        "business_phone": business_phone,
                        "business_disc": business_disc,
                        "registered": True,
                        "cart_phone": cart_phone,
                    }
                    users_collection.update_one({"user_id": user_id}, {"$set": user})
                    await event.reply(bot_text["info_saved"], buttons=Button.clear())
            else:
                parameters = text.split(" ")
                if len(parameters) > 1:
                    if parameters[0] == "/start":
                        command = parameters[1]
                        if command.startswith("image"):
                            detail_command = command.split("-")
                            get_post_id = None if len(detail_command) < 2 else detail_command[1]
                            if get_post_id is None or get_post_id == "" or len(get_post_id) < 20:
                                await event.reply(bot_text["error"])
                                return
                            else:
                                try:
                                    find_post = post_collection.find_one({"_id": ObjectId(get_post_id)})
                                    if find_post is None:
                                        await event.reply(bot_text["error"])
                                        return
                                    else:
                                        post_images = find_post["files"]
                                        if len(post_images) == 0:
                                            await event.reply(bot_text["do_not_image"])
                                            return
                                        else:
                                            r = await event.reply(bot_text["sending_images"])
                                            await bot.send_message(user_id, bot_text["show_more_images"], file=post_images)
                                            await r.delete()
                                            return 
                                except:
                                    await event.reply(bot_text["error"])
                                    return
                        elif command.startswith("cart"):
                            detail_command = command.split("-")
                            get_user_id = None if len(detail_command) < 2 else detail_command[1]
                            if get_user_id is None or get_user_id == "":
                                await event.reply(bot_text["error"])
                                return
                            else:
                                try:
                                    find_user = users_collection.find_one({"user_id": int(get_user_id)})
                                    print(find_user)
                                    if find_user is None:
                                        await event.reply(bot_text["error"])
                                        return
                                    else:
                                        user_name = find_user["name"]
                                        user_phone = find_user["cart_phone"]
                                        user_b_name = find_user["business_name"]
                                        user_b_disc = find_user["business_disc"]
                                        user_b_phone = find_user["business_phone"]
                                        user_is_seller = "فروشنده" if find_user["is_seller"] else "خریدار"
                                        # r = await event.reply(bot_text["sending_images"])
                                        cart_info = bot_text["cart_info"].format(name=user_name, b_name=user_b_name, phone=user_phone, b_phone=user_b_phone, b_disc=user_b_disc, is_seller=user_is_seller)
                                        await bot.send_message(user_id, cart_info, parse_mode="html")
                                        return 
                                except Exception as e:
                                    print(e)
                                    await event.reply(bot_text["error"])
                                    return
                        elif command.startswith("action"):
                            detail_command = command.split("-")
                            get_post_id = None if len(detail_command) < 2 else detail_command[1]
                            if get_post_id is None or get_post_id == "" or len(get_post_id) < 20:
                                await event.reply(bot_text["error"])
                                return
                            else:
                                try:
                                    find_post = post_collection.find_one({"_id": ObjectId(get_post_id)})
                                    if find_post is None:
                                        await event.reply(bot_text["error"])
                                        return
                                    else:
                                        post_user_id = find_post["user_id"]
                                        if int(user_id) == int(post_user_id):
                                            await event.reply(bot_text["cant_send_self"])
                                            return
                                        post_type = "موجود دارم" if find_post["post_type"] == "buy" else "⁉️ قیمت این پارچه چند ؟"
                                        name = find_user["name"]
                                        msg = {
                                            "_id": random.randint(10000, 99999),
                                            "user_id": user_id,
                                            "post_id": find_post["_id"],
                                            "text": post_type,
                                            "to_user": post_user_id,
                                        }
                                        msg = msg_coll.insert_one(msg)
                                        user_phone_action = "+" + str(find_user["phone"]) if str(find_user["phone"]).startswith("+") is False else str(find_user["phone"])
                                        btn = [
                                            [
                                                Button.url(bot_text["chat"], f"https://t.me/{user_phone_action}")
                                            ],
                                            [
                                                Button.inline(bot_text["answer_msg"], str.encode("answer_msg:" + str(user_id) + ":" + str(find_post["_id"]) + ":" + str(msg.inserted_id)))
                                            ]
                                        ]
                                        action_text = bot_text["action_msg"].format(name=name, text=post_type, disc=find_post["caption"], msg_link=find_post["msg_link"])
                                        await bot.send_message(post_user_id, action_text, parse_mode="html", buttons=btn, link_preview=False)
                                        await bot.send_message(user_id, bot_text["action_sent"])
                                        return
                                except Exception as e:
                                    print(e)
                                    await event.reply(bot_text["error"])
                                    return
                        else:
                            pass
                else:
                    await event.reply(bot_text["select"], buttons=main_buttons)
    elif text == bot_text["buy"] or text == bot_text["sale"]:
        async with bot.conversation(user_id, timeout=1000) as conv:
            has_image_btns = [
                [
                    Button.inline(bot_text["yes"], b'yes'),
                ],
                [
                    Button.inline(bot_text["no"], b'no')
                ],
                [
                    Button.inline(bot_text["cancel"], b'cancel')
                ]
            ]
            await conv.send_message(bot_text["has_image"], buttons=has_image_btns)
            select1 = await conv.wait_event(events.CallbackQuery())
            select = select1.data
            has_image = True
            image = None
            title = text
            post_disc = None
            has_album = False
            if select == b'no':
                has_image = False
                image = config.buy_image if text == bot_text["buy"] else config.sale_image
                await select1.delete()
            elif select == b'cancel':
                await select1.answer(bot_text["canceled"])
                await select1.delete()
                # await conv.send_message(bot_text["canceled"])
                return
            else:
                await select1.delete()
            if has_image:
                await conv.send_message(bot_text["enter_post_file"])
                image = await conv.get_response()
                image = image.media
                if image is None:
                    await conv.send_message(bot_text["error_media"])
                    return
                else:
                    image = await bot.download_media(image)
                    mime = mimetypes.guess_type(image)[0]
                    if mime.startswith("video") or mime.startswith("image"):
                        pass
                    else:
                        await conv.send_message(bot_text["error_media"])
                        return                    
            album_files = []
            await conv.send_message(bot_text["has_album"], buttons=has_image_btns)
            select1 = await conv.wait_event(events.CallbackQuery())
            select = select1.data
            if select == b'yes':
                has_album = True
                await select1.delete()
            elif select == b'cancel':
                await select1.answer(bot_text["canceled"])
                await select1.delete()
                return
            else:
                await select1.delete()
            if has_album:
                album_count = 1
                while has_album:
                    album_text = bot_text["enter_album_image"].format(count=album_count)
                    await conv.send_message(album_text)
                    album_image = await conv.get_response()
                    album_image = album_image.media
                    if album_image is None:
                        await conv.send_message(bot_text["error_media"])
                        return
                    else:
                        album_image = await bot.download_media(album_image)
                        album_files.append(album_image)
                        await conv.send_message(bot_text["has_another_image"], buttons=has_image_btns)
                        select1 = await conv.wait_event(events.CallbackQuery())
                        select = select.data
                        if select == b'no':
                            has_album = False
                            await select1.delete()
                            break
                        elif select == b'cancel':
                            await select1.answer(bot_text["canceled"])
                            await select1.delete()
                            return
                        else:
                            await select1.delete()
                        album_count += 1
            album_count = 0
            await conv.send_message(bot_text["enter_post_disc"])
            post_disc = await conv.get_response()
            post_disc = post_disc.raw_text
            post_caption = bot_text["post_caption"].format(title=title, caption=post_disc)
            post_data = {
                "user_id": user_id,
                "main_image": image,
                "caption": post_caption[:post_caption.rfind("\n")],
                "files": album_files,
                "post_type": "buy" if text == bot_text["buy"] else "sale",
                "conf": False,
                "in_channel": False,
                "msg_link": None,
                "admin_conf": False,
            }
            post = post_collection.insert_one(post_data)
            post_id = post.inserted_id
            conf_btn = [Button.inline(bot_text["conf_btn"], str.encode("conf_post:" + str(post_id)))]
            r = await event.reply(bot_text["sending_post_pre"])
            await bot.send_message(user_id, post_caption, buttons=conf_btn, file=image, parse_mode="html")
            await r.delete()

@bot.on(events.CallbackQuery(data=b'rule_yes'))
async def rule_yes(event):
    user_id = event.sender_id
    find_user = users_collection.find_one({"user_id": user_id})
    if find_user is None:
        await event.delete()
        user = {
            "user_id": user_id,
            "rule_text": bot_text["rule"],
            "is_seller": None,
            "name": None,
            "business_name": None,
            "phone": None,
            "business_phone": None,
            "business_disc": None,
            "registered": False,
            "cart_phone": None,
        }
        users_collection.insert_one(user)
        async with bot.conversation(user_id, timeout=1000) as conv:
            job_btn = [
                [
                    Button.inline(bot_text["seller"], b'seller'),
                ],
                [
                    Button.inline(bot_text["buyer"], b'buyer')
                ],
            ]
            cancel_btn = [Button.inline(bot_text["cancel"], b'cancel')]
            job_btn.append(cancel_btn)
            await conv.send_message(bot_text["select"], buttons=job_btn)
            response1 = await conv.wait_event(events.CallbackQuery())
            response = response1.data
            is_seller = False
            if response == b'cancel':
                await response1.answer(bot_text["canceled"])
                await response1.delete()
                return
            if response == b'seller':
                is_seller = True
                await response1.delete()
            else:
                await response1.delete()
            text_cancel_btn = [Button.text(bot_text["cancel"], resize=True)]
            phone_btns = [
                [
                    Button.request_phone(bot_text["share_phone"], resize=True)
                ],
                text_cancel_btn
            ]
            await conv.send_message(bot_text["share_phone_info"], buttons=phone_btns)
            phone = await conv.get_response()
            if phone.raw_text == bot_text["cancel"]:
                await conv.send_message(bot_text["canceled"], buttons=Button.clear())
                return
            phone = phone.media
            if phone is None or type(phone) != types.MessageMediaContact:
                await event.reply(bot_text["error_phone"])
                return
            phone = phone.phone_number
            await conv.send_message(bot_text["enter_name"], buttons=text_cancel_btn)
            name = await conv.get_response()
            name = name.raw_text
            if name == bot_text["cancel"]:
                await conv.send_message(bot_text["canceled"], buttons=Button.clear())
                return
            await conv.send_message(bot_text["enter_business_name"], buttons=text_cancel_btn)
            business_name = await conv.get_response()
            business_name = business_name.raw_text
            if business_name == bot_text["cancel"]:
                await conv.send_message(bot_text["canceled"], buttons=Button.clear())
                return
            await conv.send_message(bot_text["enter_phone_number"], buttons=text_cancel_btn)
            cart_phone = await conv.get_response()
            cart_phone = cart_phone.raw_text
            if cart_phone == bot_text["cancel"]:
                await conv.send_message(bot_text["canceled"], buttons=Button.clear())
                return
            await conv.send_message(bot_text["enter_business_phone"], buttons=text_cancel_btn)
            business_phone = await conv.get_response()
            business_phone = business_phone.raw_text
            if business_phone == bot_text["cancel"]:
                await conv.send_message(bot_text["canceled"], buttons=Button.clear())
                return
            await conv.send_message(bot_text["enter_business_disc"], buttons=text_cancel_btn)
            business_disc = await conv.get_response()
            business_disc = business_disc.raw_text
            if business_disc == bot_text["cancel"]:
                await conv.send_message(bot_text["canceled"], buttons=Button.clear())
                return
            user = {
                "is_seller": is_seller,
                "name": name,
                "business_name": business_name,
                "phone": phone,
                "business_phone": business_phone,
                "business_disc": business_disc,
                "registered": True,
                "cart_phone": cart_phone,
            }
            users_collection.update_one({"user_id": user_id}, {"$set": user})
            await event.reply(bot_text["info_saved"], buttons=Button.clear())
    else:
        await event.reply(bot_text["rule_before_conf"])
@bot.on(events.CallbackQuery(data=b'rule_no'))
async def rule_no(event):
    user_id = event.sender_id
    find_user = users_collection.find_one({"user_id": user_id})
    if find_user is None:
        await event.reply(bot_text["rule_not_conf"])
    else:
        await event.reply(bot_text["rule_before_conf"])
@bot.on(events.CallbackQuery(pattern="conf_post:*"))
async def conf_post(event):
    user_id = event.sender_id
    post_id = event.data.decode().split(":")[1]
    find_post = post_collection.find_one({"_id": ObjectId(post_id)})
    if find_post is None:
        await event.reply(bot_text["post_not_found"])
    else:
        await event.delete()
        post_caption = find_post["caption"]
        post_image = find_post["main_image"]
        find_phone = users_collection.find_one({"user_id": user_id})["phone"]
        find_phone = "+" + str(find_phone) if str(find_phone).startswith("+") is False else find_phone
        r = await event.reply(bot_text["sending_post"])
        s = await bot.send_message(config.CHANNEL_ID, post_caption, file=post_image, parse_mode="html")
        await r.delete()
        post_collection.update_one({"_id": ObjectId(post_id)}, {"$set": {"conf": True, "in_channel": True, "msg_link": config.CHANNEL_LINK + str(s.id)}})
        btns = [
            [
                Button.inline(bot_text["delete_post"], str.encode("delete_post:" + str(find_post["_id"])))
            ]
        ]
        await event.reply(bot_text["post_sent"], buttons=btns)
        for admin in config.ADMINS:
            await bot.send_message(admin, bot_text["post_notif"].format(post_link=config.CHANNEL_LINK + str(s.id)), buttons=[Button.inline(bot_text["delete_post"], str.encode("delete_post:" + str(find_post["_id"]))), Button.inline(bot_text["conf_post"], str.encode("conf_admin_post:" + str(find_post["_id"])))])
        await bot.send_message(config.CHANNEL_ID, file="images/sticker.webp")
@bot.on(events.CallbackQuery(pattern="answer_msg:*"))
async def answer_msg(event):
    user_id_get = event.data.decode().split(":")[1]
    post_id = event.data.decode().split(":")[2]
    msg_id = event.data.decode().split(":")[3]
    find_user_get = users_collection.find_one({"user_id": int(user_id_get)})
    if find_user_get is None:
        await event.reply(bot_text["user_not_found"])
        return
    user_id = event.sender_id
    async with bot.conversation(user_id, timeout=1000) as conv:
        await conv.send_message(bot_text["enter_answer"], buttons=Button.text(bot_text["cancel"], resize=True))
        answer = await conv.get_response()
        if answer.media is not None:
            await conv.send_message(bot_text["error_chat_media"])
        answer = answer.text
        if answer == bot_text["cancel"]:
            await conv.send_message(bot_text["canceled"], buttons=Button.clear())
            return
        find_user = users_collection.find_one({"user_id": int(user_id)})
        if find_user is None:
            await conv.send_message(bot_text["user_not_found"])
            return
        user_phone = "+" + str(find_user["phone"]) if str(find_user["phone"]).startswith("+") is False else str(find_user["phone"])
        find_post = post_collection.find_one({"_id": ObjectId(post_id)})
        if find_post is None:
            await conv.send_message(bot_text["post_not_found"])
            return
        btn = [
            [
                Button.url(bot_text["chat"], f"https://t.me/{user_phone}")
            ],
            [
                Button.inline(bot_text["answer_msg"], str.encode("answer_msg:" + str(user_id) + ":" + str(find_post["_id"]) + ":" + msg_id))
            ]
        ]
        msg_ = bot_text["answer_text"].format(name=find_user["name"], disc=find_post["caption"], msg_link=find_post["msg_link"])
        find_answers = answers_coll.find({"msg_id": msg_id}).sort("stamp")
        for m in find_answers:
            mt = bot_text["msg"].format(sender=m["user_name"], text=m["text"])
            msg_ += mt
        msg_ += "\n" + f'<blockquote>{find_user["name"]}: <b>{answer}</b></blockquote>'
        answer_insert = {
            "user_id": user_id,
            "to_user": user_id_get,
            "msg_id": msg_id,
            "text": answer,
            "user_name": find_user["name"],
            "stamp": int(time.time()),
        }
        answers_coll.insert_one(answer_insert)
        await bot.send_message(int(user_id_get), msg_, buttons=btn, link_preview=False)
        await event.reply(bot_text["answer_sent"], buttons=Button.clear())
@bot.on(events.CallbackQuery(pattern="delete_post:*"))
async def delete_post(event):
    user_id = event.sender_id
    post_id = event.data.decode().split(":")[1]
    find_post = post_collection.find_one({"_id": ObjectId(post_id)})
    if find_post is None:
        await event.reply(bot_text["post_not_found"])
        return
    if user_id in config.ADMINS or int(find_post["user_id"]) == int(user_id):
        post_collection.delete_one({"_id": ObjectId(post_id)})
        await bot.delete_messages(config.CHANNEL_ID, int(find_post["msg_link"].split("/")[-1]))
        await bot.delete_messages(config.CHANNEL_ID, int(find_post["msg_link"].split("/")[-1]) + 1)
        await event.reply(bot_text["suc_del"])
    else:
        await event.reply(bot_text["access_d"])
@bot.on(events.CallbackQuery(pattern="conf_admin_post:*"))
async def admin_post(event):
    post_id = event.data.decode().split(":")[1]
    find_post = post_collection.find_one({"_id": ObjectId(post_id)})
    if find_post is None:
        await event.reply(bot_text["post_not_found"])
        return
    if find_post["admin_conf"]:
        await event.reply(bot_text["before_conf"])
        return
    post_collection.update_one({"_id": ObjectId(post_id)}, {"$set": {"admin_conf": True}})
    first_section_btn = [

    ]
    if len(find_post["files"]) != 0:
        first_section_btn.append([Button.url(bot_text["show_more_images"], f"https://t.me/{config.BOT_ID}?start=image-{post_id}")])
    find_user = users_collection.find_one({"user_id": find_post["user_id"]})
    if find_user is None:
        await event.reply(bot_text["user_not_found"])
        return
    user_phone = str(find_user["phone"])
    phone = "+" + user_phone if user_phone.startswith("+") is False else user_phone
    post_type = "موجود دارم" if find_post["post_type"] == "buy" else "قیمت این پارچه چند⁉"
    buttons = [
        [
            Button.url(bot_text["chat"], f"https://t.me/{phone}"),
            Button.url(bot_text["cart"], f"https://t.me/{config.BOT_ID}?start=cart-{find_post["user_id"]}"),
        ],
        [
            Button.url(post_type, f"https://t.me/{config.BOT_ID}?start=action-{post_id}"),
        ]
    ]
    await bot.edit_message(config.CHANNEL_ID, int(find_post["msg_link"].split("/")[-1]), find_post["caption"] + "\n" + f'<a href="{config.CHANNEL_LINK}"> 🎯 «تار و پود»  مرجع معرفی و خرید پارچه</a>', buttons=buttons, parse_mode="html")
    await event.reply(bot_text["conf_post_suc"])
bot.run_until_disconnected()
