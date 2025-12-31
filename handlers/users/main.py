from aiogram import Router,F
from aiogram.types import CallbackQuery,InputMediaPhoto,ReplyKeyboardRemove
from utils.language import t
from keyboards.inline.buttons import main_kb
from aiogram.types import FSInputFile


router = Router()


# #________________________________________________ Back to Menu __________________________________________________
@router.callback_query(F.data == "main")
async def Menu_level(call: CallbackQuery):
    telegram_id = call.from_user.id

    main_text = await t(telegram_id, 'main_menu')
    photo = FSInputFile("media/logo.jpg")

    await call.message.edit_media(
        InputMediaPhoto(
            media=photo,
            caption=main_text
        ),
        reply_markup=await main_kb(telegram_id)
    )



# #________________________________________________ Work With Booking _______________________________________________





# #________________________________________________ Work With Payment ___________________________________________________

# @router.callback_query(F.data == "payment")
# async def Payment_level(call: CallbackQuery):
# 	banners = await db.select_banners()
# 	for banner in banners:
# 		if banner['name'] == "payment":
# 			await call.message.edit_media(InputMediaPhoto(media=banner['photo_id'],caption=f"With credit card ✅\nWith cash ✅\nWhen you take it ✅"),
# 			reply_markup=main)

# #______________________________________________ Work with Cart  _______________________________________________________


# @router.callback_query(F.data == "cart")
# async def Cart_level(call: CallbackQuery):
# 	user_id = call.from_user.id
# 	products= await db.select_cart_products(user_id=user_id)
# 	if not products:
# 		banners = await db.select_banners()
# 		for banner in banners:
# 			if banner['name'] == "cart":
# 				await call.message.edit_media(InputMediaPhoto(media=f"{banner['photo_id']}",caption=f"there is nothing ❌ \nYou must add product to use ! "),reply_markup=main_page)
# 	else:		
# 		raqam = 0
# 		product = products[raqam]

# 		await call.message.edit_media(
# 			InputMediaPhoto(media=product['image'], caption=caption(products=products,raqam=raqam)),
# 			reply_markup=await Get_product_frm_cart(user_id=user_id, raqam=raqam)
# 		)

# @router.callback_query(F.data.startswith("cartpage_"))       
# async def Cart_level_2(call: CallbackQuery):
# 	raqam = int(call.data.split("_")[1])
# 	user_id = call.from_user.id
# 	products= await db.select_cart_products(user_id=user_id)
# 	product = products[raqam]
	
# 	await call.message.edit_media(
# 		InputMediaPhoto(media=product['image'], caption=caption(products=products,raqam=raqam)),
# 		reply_markup=await Get_product_frm_cart(user_id=user_id, raqam=raqam)
# 	)


# @router.callback_query(F.data.startswith("productid_"))
# async def Delete_cart_product(call: CallbackQuery):
# 	product_id = int(call.data.split("_")[1])
# 	raqam = int(call.data.split("_")[2])
# 	user_id = call.from_user.id

# 	await db.delete_cart_product(product_id=product_id)
# 	products = await db.select_cart_products(user_id=user_id)

# 	if not products:
# 		banners = await db.select_banners()
# 		for banner in banners:
# 			if banner['name'] == "cart":
# 				await call.message.edit_media(InputMediaPhoto(media=f"{banner['photo_id']}",caption=f"there is nothing ❌ \nYou must add product to use ! "),reply_markup=main_page)
# 	else:		
# 		raqam = 0
# 		product = products[raqam]

# 		await call.message.edit_media(
# 			InputMediaPhoto(media=product['image'], caption=caption(products=products,raqam=raqam)),
# 			reply_markup=await Get_product_frm_cart(user_id=user_id, raqam=raqam)
# 		)


# @router.callback_query(F.data.startswith("+_"))
# async def Quantity_plus(call: CallbackQuery):
# 	user_id = call.from_user.id
# 	product_id= int(call.data.split("_")[1])
# 	raqam = int(call.data.split("_")[2])
# 	await db.cart_plus_quantity(user_id=user_id,product_id=product_id)
	
# 	products= await db.select_cart_products(user_id=user_id)
# 	product = products[raqam]
	
# 	await call.message.edit_media(
# 		InputMediaPhoto(media=product['image'], caption=caption(products=products,raqam=raqam)),
# 		reply_markup=await Get_product_frm_cart(user_id=user_id, raqam=raqam)
# 	)


# @router.callback_query(F.data.startswith("-_"))
# async def Quantity_minus(call: CallbackQuery):
# 	user_id = call.from_user.id
# 	product_id= int(call.data.split("_")[1])
# 	raqam = int(call.data.split("_")[2])
# 	await db.cart_minus_quantity(user_id=user_id,product_id=product_id)
	
# 	products= await db.select_cart_products(user_id=user_id)
# 	product = products[raqam]

# 	await call.message.edit_media(
# 		InputMediaPhoto(media=product['image'], caption=caption(products=products,raqam=raqam)),
# 		reply_markup=await Get_product_frm_cart(user_id=user_id, raqam=raqam)
# 	)
# #______________________________________________ Work with Dilivery  _______________________________________________________
# @router.callback_query(F.data == "dilivery")
# async def Diliver_level(call: CallbackQuery):
# 	banners = await db.select_banners()
# 	caption = (
#     "🚚 Delivery Options\n"
#     "You can choose one of the following delivery methods:\n"
#     "🏍 Courier delivery\n"
#     "🚖 Taxi delivery\n"
#     "🏠 Pick up by yourself ✅\n\n"
#     "⚠️ Delivery is not available with birds or dogs. 🐦🐕"
# 	)

# 	for banner in banners:
# 		if banner['name'] == "dilivery":
# 			await call.message.edit_media(InputMediaPhoto(media=banner['photo_id'],caption=caption),reply_markup=main)


# #______________________________________________ Work with ORder  _______________________________________________________

# # @router.callback_query(F.data.startswith("order_"))
# # async def Order_level(call: CallbackQuery, state: FSMContext):
# #     product_id = int(call.data.split("_")[1])
# #     user_id = call.from_user.id
# #     product = await db.select_cart_product(user_id=user_id, product_id=product_id)


# #     qty = int(product['quantity'])
# #     price = float(product['price'])
# #     total = price * qty

# #     caption = (
# #         f"🍕 <b>{product['name']}</b>\n"
# #         f"{product['description']}\n\n"
# #         f"💲 Price: ${price:.2f}\n"
# #         f"🔢 Quantity: {qty}\n"
# #         f"💰 Sum: ${total:.2f}\n\n"
# #         f"Please send your <b>name</b> ✍️"
# #     )

# #     await call.message.answer_photo(photo=product['image'], caption=caption, parse_mode="HTML")
# #     await state.update_data(product=product, total=total)
# #     await state.set_state(OrderState.name)



# # @router.message(OrderState.name)
# # async def Name_State_answer(message: Message, state: FSMContext):
# #     await state.update_data(name=message.text.strip())
# #     await message.answer("✅ Got it!\nNow please send me your contact 📞", reply_markup=contact_btn)
# #     await state.set_state(OrderState.contact)


# # @router.message(OrderState.contact, F.contact)
# # async def Contact_State_answer(message: Message, state: FSMContext):
# #     phone = message.contact.phone_number
# #     await state.update_data(contact=phone)
# #     await message.answer("✅ Contact received!\nNow please send me your location 📍", reply_markup=location_btn)
# #     await state.set_state(OrderState.location)


# # @router.message(OrderState.location, F.location)
# # async def Location_State_answer(message: Message, state: FSMContext):
# #     lon = message.location.longitude
# #     lat = message.location.latitude
# #     await state.update_data(longitude=lon, latitude=lat)

# #     data = await state.get_data()
# #     name = data['name']
# #     phone = data['contact']

# #     await message.answer(
# #         f"✅ Check your information:\n\n"
# #         f"👤 Name: {name}\n"
# #         f"📞 Phone: {phone}\n\n"
# #         f"Do you confirm your order?",
# #         reply_markup=ReplyKeyboardRemove() 
# #     )
# #     await state.set_state(OrderState.confirm)


# # @router.callback_query(OrderState.confirm)
# # async def confirm_order(call: CallbackQuery, state: FSMContext):
# #     if call.data == "yes":
# #         data = await state.get_data()
# #         name = data["name"]
# #         phone = data["contact"]
# #         lat = data["latitude"]
# #         lon = data["longitude"]
# #         product = data["product"]
# #         total = data["total"]

       
# #         admin_text = (
# #             f"📦 <b>New Order!</b>\n\n"
# #             f"🍕 <b>{product['name']}</b>\n"
# #             f"{product['description']}\n\n"
# #             f"💲 Price: ${product['price']}\n"
# #             f"🔢 Quantity: {product['quantity']}\n"
# #             f"💰 Total: ${total:.2f}\n\n"
# #             f"👤 <b>Name:</b> {name}\n"
# #             f"📞 <b>Phone:</b> {phone}"
# #         )

  
# #         for admin_id in ADMINS:
# #             await call.bot.send_message(admin_id, admin_text, parse_mode="HTML")
# #             await call.bot.send_location(admin_id, latitude=lat, longitude=lon)

# #         await call.message.edit_text("✅ Your order is accepted! We'll contact you soon.")
# #         await state.clear()

# #     elif call.data == "no":
# #         await call.message.edit_text("❌ Order canceled.")
# #         await state.clear()