from django.shortcuts import render,redirect
from ecommerceapp.models import Contact,Product,OrderUpdate,Orders
from django.contrib import messages
from math import ceil
from django.conf import settings
import json
from django.views.decorators.csrf import  csrf_exempt

# Create your views here.
def index(request):

    allProds = []
    catprods = Product.objects.values('category','id')
    print(catprods)
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod= Product.objects.filter(category=cat)
        n=len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params= {'allProds':allProds}

    return render(request,"index.html",params)

    
def contact(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        desc=request.POST.get("desc")
        pnumber=request.POST.get("pnumber")
        myquery=Contact(name=name,email=email,desc=desc,phonenumber=pnumber)
        myquery.save()
        messages.info(request,"we will get back to you soon..")
        return render(request,"contact.html")


    return render(request,"contact.html")

def about(request):
    return render(request,"about.html")

# def razor(request):
#     return render(request,"razor.html")


# def checkout(request):
#     if not request.user.is_authenticated:
#         messages.warning(request,"Login & Try Again")
#         return redirect('/auth/login')

#     if request.method=="POST":
#         items_json = request.POST.get('itemsJson', '')
#         name = request.POST.get('name', '')
#         amount = request.POST.get('amt')
#         email = request.POST.get('email', '')
#         address1 = request.POST.get('address1', '')
#         address2 = request.POST.get('address2','')
#         city = request.POST.get('city', '')
#         state = request.POST.get('state', '')
#         zip_code = request.POST.get('zip_code', '')
#         phone = request.POST.get('phone', '')
#         Order = Orders(items_json=items_json,name=name,amount=amount, email=email, address1=address1,address2=address2,city=city,state=state,zip_code=zip_code,phone=phone)
#         print(amount)
#         Order.save()
#         update = OrderUpdate(order_id=Order.order_id,update_desc="the order has been placed")
#         update.save()
#         thank = True
        
#     return render(request, 'checkout.html')



def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/auth/login')

    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amt')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        # Calculate the amount in paise
        total_amount_in_paise = int(float(amount) * 100)

        Order = Orders(items_json=items_json, name=name, amount=amount, email=email, address1=address1,
                       address2=address2, city=city, state=state, zip_code=zip_code, phone=phone)
        Order.save()

        update = OrderUpdate(order_id=Order.order_id, update_desc="the order has been placed")
        update.save()

        thank = True
        context = {'total_amount_in_paise': total_amount_in_paise}
        return render(request, 'checkout.html', context)

    return render(request, 'checkout.html')


# # PAYMENT INTEGRATION

#         id = Order.order_id
#         oid=str(id)+"SkullCandy"
#         param_dict = {

#             # 'MID':keys.MID,
#             'ORDER_ID': oid,
#             'TXN_AMOUNT': str(amount),
#             'CUST_ID': email,
#             'INDUSTRY_TYPE_ID': 'Retail',
#             'WEBSITE': 'WEBSTAGING',
#             'CHANNEL_ID': 'WEB',
#             'CALLBACK_URL': 'http://127.0.0.1:4444/handlerequest/',

#         }
#         # param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
#         return render(request, 'paytm.html', {'param_dict': param_dict})

#     return render(request, 'checkout.html')


# @csrf_exempt
# def handlerequest(request):
#     # paytm will send you post request here
#     form = request.POST
#     response_dict = {}
#     for i in form.keys():
#         response_dict[i] = form[i]
#         if i == 'CHECKSUMHASH':
#             checksum = form[i]

#     verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
#     if verify:
#         if response_dict['RESPCODE'] == '01':
#             print('order successful')
#             a=response_dict['ORDERID']
#             b=response_dict['TXNAMOUNT']
#             rid=a.replace("ShopyCart","")
           
#             print(rid)
#             filter2= Orders.objects.filter(order_id=rid)
#             print(filter2)
#             print(a,b)
#             for post1 in filter2:

#                 post1.oid=a
#                 post1.amountpaid=b
#                 post1.paymentstatus="PAID"
#                 post1.save()
#             print("run agede function")
#         else:
#             print('order was not successful because' + response_dict['RESPMSG'])
#     return render(request, 'paymentstatus.html', {'response': response_dict})


# def profile(request):
#     if not request.user.is_authenticated:
#         messages.warning(request,"Login & Try Again")
#         return redirect('/auth/login')
#     currentuser=request.user.username
#     items=Orders.objects.filter(email=currentuser)
#     rid=""
#     for i in items:
#         print(i.oid)
#         print(i.order_id)
#         myid=i.oid
#         rid=myid.replace("skullcandy","")
#         print(rid)
#     status=OrderUpdate.objects.filter(order_id=int(rid))
#     for j in status:
#         print(j.update_desc)

   
#     context ={"items":items,"status":status}
#     print(currentuser)
#     return render(request,"profile.html",context)

def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect('/auth/login')

    currentuser = request.user.email
    items = Orders.objects.filter(email=currentuser)
    if not items.exists():
        messages.info(request, "No orders found for this user.")
        return render(request, "profile.html", {"items": None, "status": None})

    order_ids = [item.order_id for item in items]
    status = OrderUpdate.objects.filter(order_id__in=order_ids)

    context = {"items": items, "status": status}
    return render(request, "profile.html", context)




# def profile(request):
#     if not request.user.is_authenticated:
#         messages.warning(request, "Login & Try Again")
#         return redirect('/auth/login')
    
#     currentuser = request.user.username
#     items = Orders.objects.filter(email=currentuser)
#     rid = ""
#     for i in items:
#         print(i.oid)
#         myid = i.oid
#         rid = myid.replace("Skullcandy", "")
#         print(rid)

#     if not rid:
#         # Handle case where rid is empty
#         messages.error(request, "Order ID not found.")
#         return redirect('/')

#     try:
#         rid_int = int(rid)
#         status = OrderUpdate.objects.filter(order_id=rid_int)
#     except ValueError:
#         # Handle case where rid is not a valid integer
#         messages.error(request, "Invalid order ID.")
#         return redirect('/')

#     for j in status:
#         print(j.update_desc)

#     context = {"items": items, "status": status}
#     print(currentuser)
#     return render(request, "profile.html", context)
    
