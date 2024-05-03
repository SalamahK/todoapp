from django.http import Http404, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from .models import TodoList, Category
from .forms import CategoryForm

urls = {
    "category_url" : 'http://127.0.0.1:8000/todos/category',
    "todo_url": 'http://127.0.0.1:8000/todos',
}
def index(request): #the index view
    todos = TodoList.objects.all() #quering all todos with the object manager
    categories = Category.objects.all() #getting all categories with object manager

    if request.method == "POST": #checking if the request method is a POST
        if "taskAdd" in request.POST: #checking if there is a request to add a todo
            title = request.POST["description"] #title
            date = str(request.POST["date"]) #date
            category = request.POST["category_select"] #category
            content = title + " -- " + date + " " + category #content
            Todo = TodoList(title=title, content=content, due_date=date, category=Category.objects.get(name=category))
            Todo.save() #saving the todo 
            return redirect("/todos") #reloading the page
        if "taskDelete" in request.POST: #checking if there is a request to delete a todo
            checkedlist = request.POST["checkedbox"] #checked todos to be deleted
            for todo_id in checkedlist:
                todo = TodoList.objects.get(id=int(todo_id)) #getting todo id
                todo.delete() #deleting todo

    return render(request, "index.html", {"todos": todos,  "categories":categories, "url": urls})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todoapp:index')  # Redirect to the index page after adding a category
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})

def category(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        # if "addCategory" in request.POST:
        #     category_name = request.POST['category']
        #     if Category.objects.filter(name=category_name).exists():
        #         raise Http404("Category already exists")
        #     new_category = Category(name=category_name)
        #     new_category.save()
        #     return redirect("/todos/category")
        
        if "deleteCategory" in request.POST:
            category_id = int(request.POST.get("deleteCategory"))
            category_to_delete = Category.objects.get(id=category_id)
            category_to_delete.delete()
            return redirect("/todos/category")
    context = {
        "categories" : categories,
        "url": urls
    }
    return render(request, "category.html", context)


    # return render(request, "category.html", {"categories" : categories, "url" : urls})