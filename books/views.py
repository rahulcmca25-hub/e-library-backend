from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Book
from .serializers import BookSerializer

from rest_framework.permissions import IsAuthenticated

from django.core.paginator import Paginator

from users.permissions import IsLibrarianOrAdmin

from ai.services import generate_book_summary

class BookListView(APIView):


    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]

        return [IsLibrarianOrAdmin()]

    def get(self, request):

        books = Book.objects.all()

        # ---------------- SEARCH ----------------

        search = request.query_params.get("search")

        if search:
            books = books.filter(
                Q(title__icontains=search) |
                Q(isbn__icontains=search) |
                Q(author__name__icontains=search) |
                Q(category__name__icontains=search)
            )

        # ---------------- SORTING ----------------

        ordering = request.query_params.get("ordering", "title")

        allowed_ordering = [
            "title",
            "-title",
            "published_date",
            "-published_date",
            "created_at",
            "-created_at",
        ]

        if ordering in allowed_ordering:
            books = books.order_by(ordering)

        # ---------------- PAGINATION ----------------

        page = request.query_params.get("page", 1)
        page_size = request.query_params.get("page_size", 5)

        try:
            page = int(page)
            page_size = int(page_size)
        except ValueError:
            return Response({
                "error": "page and page_size must be integers"
            }, status=400)

        if page < 1:
            page = 1

        if page_size < 1:
            page_size = 5

        if page_size > 50:
            page_size = 50

        paginator = Paginator(books, page_size)

        page_obj = paginator.get_page(page)

        serializer = BookSerializer(
            page_obj.object_list,
            many=True
        )

        return Response({
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "current_page": page_obj.number,
            "page_size": page_size,
            "results": serializer.data
        })



    # POST /api/books/
    def post(self, request):

        if request.user.role not in ["LIBRARIAN", "ADMIN"]:
            return Response(
                {"detail": "Only librarian or admin can add books"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = BookSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class BookDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):

        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return None

    # GET /api/1/
    def get(self, request, pk):

        book = self.get_object(pk)

        if not book:
            return Response(
                {"detail": "Book not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = BookSerializer(book)

        return Response(serializer.data)

    # POST /api/1/  -> don't use this
    # PUT /api/1/
    def put(self, request, pk):

        if request.user.role not in ["LIBRARIAN", "ADMIN"]:
            return Response(
                {"detail": "Only librarian or admin can update books"},
                status=status.HTTP_403_FORBIDDEN
            )

        book = self.get_object(pk)

        if not book:
            return Response(
                {"detail": "Book not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = BookSerializer(
            book,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # PATCH /api/1/
    def patch(self, request, pk):

        if request.user.role not in ["LIBRARIAN", "ADMIN"]:
            return Response(
                {"detail": "Only librarian or admin can update books"},
                status=status.HTTP_403_FORBIDDEN
            )

        book = self.get_object(pk)

        if not book:
            return Response(
                {"detail": "Book not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = BookSerializer(
            book,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE /api/1/
    def delete(self, request, pk):

        if request.user.role != "ADMIN":
            return Response(
                {"detail": "Only admin can delete books"},
                status=status.HTTP_403_FORBIDDEN
            )

        book = self.get_object(pk)

        if not book:
            return Response(
                {"detail": "Book not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        book.delete()

        return Response(
            {"detail": "Book deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

        


class BookDetailView(APIView):

    def get_permissions(self):

        if self.request.method == "GET":
            return [IsAuthenticated()]

        return [IsLibrarianOrAdmin()]

    def get(self, request):

        books = Book.objects.all()

        # -------------------------
        # SEARCH
        # -------------------------

        search = request.GET.get("search")

        if search:
            books = books.filter(
                Q(title__icontains=search)
                | Q(author__name__icontains=search)
                | Q(category__name__icontains=search)
                | Q(isbn__icontains=search)
            )

        # -------------------------
        # FILTER BY AUTHOR
        # -------------------------

        author = request.GET.get("author")

        if author:
            books = books.filter(
                author__name__icontains=author
            )

        # -------------------------
        # FILTER BY CATEGORY
        # -------------------------

        category = request.GET.get("category")

        if category:
            books = books.filter(
                category__name__icontains=category
            )

        # -------------------------
        # AVAILABLE BOOKS ONLY
        # -------------------------

        available = request.GET.get("available")

        if available == "true":
            books = books.filter(
                available_copies__gt=0
            )

        # -------------------------
        # PAGINATION
        # -------------------------

        page = int(request.GET.get("page", 1))
        limit = int(request.GET.get("limit", 10))

        start = (page - 1) * limit
        end = start + limit

        total = books.count()

        books = books[start:end]

        serializer = BookSerializer(
            books,
            many=True
        )

        return Response({
            "count": total,
            "page": page,
            "limit": limit,
            "results": serializer.data
        })

    
    # PUT /api/books/<id>/
    def put(self, request, pk):

        book = self.get_object(pk)

        if book is None:
            return Response(
                {"error": "Book not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = BookSerializer(
            book,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # PATCH /api/books/<id>/
    def patch(self, request, pk):

        book = self.get_object(pk)

        if book is None:
            return Response(
                {"error": "Book not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = BookSerializer(
            book,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE /api/books/<id>/
    def delete(self, request, pk):

        book = self.get_object(pk)

        if book is None:
            return Response(
                {"error": "Book not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        book.delete()

        return Response(
            {"message": "Book deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


# Book summery

class BookSummaryView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response(
                {"detail": "Book not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            summary = generate_book_summary(book)

            return Response({
                "book_id": book.id,
                "title": book.title,
                "summary": summary
            })

        except Exception as e:

            return Response(
                {
                    "detail": "Unable to generate summary",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )    