from django.http import Http404
from django.shortcuts import render, redirect

from .models import TodoList, Category
from .forms import CategoryForm

urls = {
    "category_url": '/todos/category',  # Updated URL
    "todo_url": '/todos',  # Updated URL
}

def index(request):
    todos = TodoList.objects.all()
    categories = Category.objects.all()

    if request.method == "POST":
        if "taskAdd" in request.POST:
            title = request.POST["description"]
            date = str(request.POST["date"])
            selected_categories = request.POST.getlist("category_select")  # Get list of selected categories
            content = title + " -- " + date + " " + ", ".join(selected_categories)
            todo = TodoList(title=title, content=content, due_date=date)
            todo.save()
            todo.categories.set(Category.objects.filter(name__in=selected_categories))  # Assign selected categories to todo
            return redirect("index")  # Redirect to the index page after adding a task
        elif "taskDelete" in request.POST:
            checkedlist = request.POST.getlist("checkedbox")
            for todo_id in checkedlist:
                todo = TodoList.objects.get(id=int(todo_id))
                todo.delete()

    return render(request, "index.html", {"todos": todos, "categories": categories, "url": urls})

def add_category(request):
    form = CategoryForm()  # Instantiate the CategoryForm

    if request.method == 'POST':
        form = CategoryForm(request.POST)  # Bind POST data to the form
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('index')  # Redirect back to the category page after adding a category

    # Pass the form to the template context
    context = {'form': form}

    return render(request, 'add_category.html', context)

def category(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        if "addCategory" in request.POST:
            category_name = request.POST['category']
            if Category.objects.filter(name=category_name).exists():
                raise Http404("Category already exists")
            new_category = Category(name=category_name)
            new_category.save()
            return redirect("/todos/category")
        elif "deleteCategory" in request.POST:
            category_ids = request.POST.getlist("deleteCategory")  # Get list of selected category IDs
            Category.objects.filter(id__in=category_ids).delete()  # Delete selected categories
            return redirect("/todos/category")

    context = {"categories": categories, "url": urls}
    return render(request, "category.html", context)
