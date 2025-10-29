# from django.contrib import messages
# from django.shortcuts import render, redirect
# from django.db import transaction
# from . import models

# def home(request):
#     return render(request, 'index.html')

# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.core.cache import cache
# import json

# # @csrf_exempt
# # def uid_api(request):
# #     if request.method == "POST":
# #         try:
# #             data = json.loads(request.body.decode())
# #             uid = data.get("uid", "").strip()
# #             if uid:
# #                 cache.set("last_uid", uid, timeout=None)
# #                 print(f"💾 UID saved: {uid}")
# #                 return JsonResponse({"status": "ok"})
# #         except Exception as e:
# #             print("POST parse error:", e)
# #         return JsonResponse({"status": "error"}, status=400)

# #     elif request.method == "GET":
# #         uid = cache.get("last_uid", "")
# #         if uid:
# #             # сразу очищаем, чтобы при следующем запросе не повторялся
# #             cache.delete("last_uid")
# #             print(f"➡️ UID sent to client: {uid} (then cleared)")
# #         return JsonResponse({"uid": uid})

# @csrf_exempt
# def uid_api(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body.decode())
#             uid = data.get("uid", "").strip()
#             if uid:
#                 cache.set("last_uid", uid, timeout=None)  # хранится до следующего запроса
#                 print(f"💾 UID saved: {uid}")
#                 return JsonResponse({"status": "ok"})
#         except Exception as e:
#             print("POST parse error:", e)
#         return JsonResponse({"status": "error"}, status=400)

#     elif request.method == "GET":
#         uid = cache.get("last_uid", "")
#         if uid:
#             print(f"➡️ UID sent to client: {uid}")
#         else:
#             print("⚠️ No UID in cache")
#         return JsonResponse({"uid": uid})



# def tables(request):
#     # Paginate the payments to avoid loading all at once
#     payments = models.Payment.objects.all().order_by('-created_at')
#     page_number = request.GET.get('page')

#     context = {
#         'payments': payments
#     }

#     if request.method == 'POST':
#         cardUID = request.POST.get('cardUID')
#         balance = request.POST.get('balance')

#         if not cardUID or not balance:
#             messages.error(request, 'Invalid input: card UID or balance missing')
#             return redirect('tables')

#         try:
#             balance = 0 if balance == '' else float(balance)

#             cardUID = cardUID[:12].replace('\"', '')

#             client = models.Client.objects.filter(rf_id=cardUID).first()

#             if not client:
#                 messages.error(request, 'Client not found')
#                 return redirect('tables')

#             if client.balance < balance:
#                 messages.error(request, 'Not enough money')
#                 return redirect('tables')

#             point = models.Point.objects.last()

#             if not point:
#                 messages.error(request, 'Point not found')
#                 return redirect('tables')

#             with transaction.atomic():
#                 payment = models.Payment.objects.create(
#                     client=client,
#                     point=point,
#                     balance=balance
#                 )
#                 client.balance -= balance
#                 point.balance += balance

#                 client.save()
#                 point.save()

#             messages.success(request, 'Payment successfully created')
#             return redirect('tables')

#         except ValueError:
#             messages.error(request, 'Invalid balance amount')
#             return redirect('tables')

#         except models.Client.DoesNotExist:
#             messages.error(request, 'Client not found')
#             return redirect('tables')

#         except models.Point.DoesNotExist:
#             messages.error(request, 'Point not found')
#             return redirect('tables')

#         except Exception as e:
#             print(f"Error during payment creation: {e}")
#             messages.error(request, 'Something went wrong. Please try again.')
#             return redirect('tables')

#     return render(request, 'tables.html', context)


# from django.shortcuts import render
# from .models import Client, Payment
# from django.core.cache import cache

# def account_view(request):
#     # Получаем UID из кэша
#     uid = cache.get("last_uid", "")
#     client = None
#     payments = []

#     if uid:
#         # Ищем клиента по UID
#         client = Client.objects.filter(rf_id=uid).first()
#         if client:
#             # Получаем последние 5 платежей
#             payments = Payment.objects.filter(client=client).order_by('-created_at')

#     return render(request, 'account.html', {
#         'client': client,
#         'uid': uid,
#         'payments': payments
#     })




# from django.core.cache import cache
# from django.http import JsonResponse
# from .models import Client, Payment

# def api_client_info(request):
#     # Получаем UID из кэша
#     uid = cache.get("last_uid", "")
#     if not uid:
#         return JsonResponse({'found': False})

#     # Ищем клиента по UID
#     client = Client.objects.filter(rf_id=uid).first()
#     if not client:
#         return JsonResponse({'found': False})

#     # Получаем последние 5 платежей
#     payments = list(
#         Payment.objects.filter(client=client)
#         .values('balance', 'created_at')
#         .order_by('-created_at')[:5]
#     )

#     # Возвращаем информацию о клиенте и его платежах
#     return JsonResponse({
#         'found': True,
#         'uid': uid,
#         'name': f"{client.first_name} {client.last_name}",
#         'balance': client.balance,
#         'payments': payments,
#     })




from django.contrib import messages
from django.shortcuts import render, redirect
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from . import models
import json


def home(request):
    return render(request, 'index.html')


@csrf_exempt
def uid_api(request):
    """
    POST: Принимает UID от ридера и сохраняет в кэш
    GET: Возвращает UID один раз, затем очищает кэш
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            uid = data.get("uid", "").strip().upper()
            if uid:
                cache.set("last_uid", uid, timeout=None)  # сохраняем
                print(f"UID saved: {uid}")
                return JsonResponse({"status": "ok"})
        except Exception as e:
            print("POST parse error:", e)
        return JsonResponse({"status": "error"}, status=400)

    elif request.method == "GET":
        uid = cache.get("last_uid")
        if uid:
            print(f"UID sent to client: {uid}")
            cache.delete("last_uid")  # ОЧИЩАЕМ ПОСЛЕ ОТПРАВКИ
        else:
            print("No UID in cache")
        return JsonResponse({"uid": uid or None})


def tables(request):
    payments = models.Payment.objects.all().order_by('-created_at')
    context = {'payments': payments}

    if request.method == 'POST':
        cardUID = request.POST.get('cardUID', '').strip()
        balance_input = request.POST.get('balance', '').strip()

        if not cardUID or not balance_input:
            messages.error(request, 'Invalid input: card UID or balance missing')
            return redirect('tables')

        try:
            balance = float(balance_input)
            if balance <= 0:
                raise ValueError()

            cardUID = cardUID[:12].replace('"', '')

            client = models.Client.objects.filter(rf_id=cardUID).first()
            if not client:
                messages.error(request, 'Client not found')
                return redirect('tables')

            if client.balance < balance:
                messages.error(request, 'Not enough money')
                return redirect('tables')

            point = models.Point.objects.last()
            if not point:
                messages.error(request, 'Point not found')
                return redirect('tables')

            with transaction.atomic():
                payment = models.Payment.objects.create(
                    client=client,
                    point=point,
                    balance=balance
                )
                client.balance -= balance
                point.balance += balance
                client.save()
                point.save()

            messages.success(request, 'Payment successfully created')
            return redirect('tables')

        except ValueError:
            messages.error(request, 'Invalid balance amount')
        except Exception as e:
            print(f"Error during payment: {e}")
            messages.error(request, 'Something went wrong.')
        return redirect('tables')

    return render(request, 'tables.html', context)


def account_view(request):
    """
    Страница аккаунта — не зависит от RFID
    Показывает заглушку, данные подгружаются через JS
    """
    return render(request, 'account.html', {
        'client': None,
        'uid': '',
        'payments': []
    })


def api_client_info(request):
    """
    API: /api/client/?uid=ABC123
    Возвращает данные клиента по UID
    """
    uid = request.GET.get('uid', '').strip().upper()
    if not uid:
        return JsonResponse({'found': False})

    client = models.Client.objects.filter(rf_id=uid).first()
    if not client:
        return JsonResponse({'found': False})

    payments = list(
        models.Payment.objects.filter(client=client)
        .values('balance', 'created_at')
        .order_by('-created_at')[:5]
    )

    return JsonResponse({
        'found': True,
        'uid': uid,
        'name': f"{client.first_name} {client.last_name}".strip(),
        'balance': float(client.balance),
        'payments': payments,
    })