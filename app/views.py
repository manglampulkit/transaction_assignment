from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum, Count
from .models import Transaction
from .serializers import TransactionSerializer
from django.shortcuts import render, redirect
from .utils import calculate_score

class TransactionCreateView(APIView):

    def post(self, request):

        serializer = TransactionSerializer(
            data=request.data
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            transaction = serializer.save()

            return Response(
                {
                    "message": "Transaction created successfully",
                    "transaction_id": transaction.transaction_id
                },
                status=status.HTTP_201_CREATED
            )

        except IntegrityError:
            return Response(
                {
                    "error": "Duplicate transaction_id. Transaction already processed."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
class UserSummaryView(APIView):

    def get(self, request, user_id):

        transactions = Transaction.objects.filter(
            user_id=user_id
        )

        if not transactions.exists():
            return Response(
                {
                    "error": "User not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        summary = transactions.aggregate(
            total_amount=Sum('amount'),
            total_transactions=Count('id')
        )

        total_amount = summary['total_amount'] or 0
        total_transactions = summary['total_transactions'] or 0

        score = (
            float(total_amount) * 0.6
            + total_transactions * 20
        )

        return Response(
            {
                "user_id": user_id,
                "total_transactions": total_transactions,
                "total_amount": float(total_amount),
                "score": round(score, 2)
            }
        )

class RankingView(APIView):

    def get(self, request):

        users = (
            Transaction.objects
            .values('user_id')
            .annotate(
                total_amount=Sum('amount'),
                total_transactions=Count('id')
            )
        )

        rankings = []

        for user in users:

            score = (
                float(user['total_amount']) * 0.6
                + user['total_transactions'] * 20
            )

            rankings.append({
                "user_id": user['user_id'],
                "total_amount": float(user['total_amount']),
                "total_transactions": user['total_transactions'],
                "score": round(score, 2)
            })

        rankings.sort(
            key=lambda x: x['score'],
            reverse=True
        )

        for index, user in enumerate(rankings, start=1):
            user["rank"] = index

        return Response(rankings)


def home_page(request):

    message = None

    if request.method == "POST":

        transaction_id = request.POST.get("transaction_id")
        user_id = request.POST.get("user_id")
        amount = request.POST.get("amount")

        try:
            Transaction.objects.create(
                transaction_id=transaction_id,
                user_id=user_id,
                amount=amount
            )

            message = "Transaction created successfully."

        except Exception:
            message = "Duplicate transaction ID."

    return render(
        request,
        "app/home.html",
        {"message": message}
    )

def summary_page(request):

    data = None

    if request.method == "POST":

        user_id = request.POST.get("user_id")

        transactions = Transaction.objects.filter(
            user_id=user_id
        )

        if transactions.exists():

            summary = transactions.aggregate(
                total_amount=Sum("amount"),
                total_transactions=Count("id")
            )

            total_amount = float(summary["total_amount"])
            total_transactions = summary["total_transactions"]

            score = (
                total_amount * 0.6
                + total_transactions * 20
            )

            data = {
                "user_id": user_id,
                "total_amount": total_amount,
                "total_transactions": total_transactions,
                "score": round(score, 2)
            }

    return render(
        request,
        "app/summary.html",
        {"data": data}
    )

def ranking_page(request):

    users = (
        Transaction.objects
        .values("user_id")
        .annotate(
            total_amount=Sum("amount"),
            total_transactions=Count("id")
        )
    )

    rankings = []

    for user in users:

        score = calculate_score(
                user["total_amount"],
                user["total_transactions"]
            )
        rankings.append({
            "user_id": user["user_id"],
            "total_amount": float(user["total_amount"]),
            "total_transactions": user["total_transactions"],
            "score": round(score, 2)
        })

    rankings.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    for index, user in enumerate(rankings, start=1):
        user["rank"] = index

    return render(
        request,
        "app/ranking.html",
        {"rankings": rankings}
    )