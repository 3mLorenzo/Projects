-- Youtube link:
    here

-- Main idea
    The main idea for this project is to create a web app using Javascript, Python and the framework that we used in this whole course, that is Django. The web-app consists of a task managing app, a place that you can create your tasks and work on them until the deadline. I had this idea because I myself have issues on working uniformlly and not doing everything on the last day. I think managing your time is very import and is also very normal if you need help with it. Hence, the web-app I made. The main idea for the app was for it to remain simple, so that people don´t waste their time creating tasks instead of doing them. The main components of the app are:
        - A main page that can be accessed be anyone (base.html)
        - A login, Logout and register function copied from project 4 (changed the CSS a little)
        - Every other page can only be accessed if you login/register
            - A page where there is a list of all your tasks (in this page you can create new tasks)
            - Clicking on a task will render a task details page, where you can edit, delete and mark as completed the specific task
            - A page that will display a list of all categories that you created.
            - Clicking on a category will render its details page, there you can edit or delete your category

-- Distinctiveness and Complexity
    I do not believe a page with similar ideas was created as projects during this course. It is not an e-commerce and it´s also not a social media app.
    
    In terms of complexity I have using more than one Django model (class Task and class Category) and I have used also more than one django forms (CategoryForm and TaskForm). In addition to that, the app is screensize responsive, as it will shrink for smaller screens (cellphones for example).

-- Files information
    In views.py there is all the backend code. Apart from login/register and index all the views function are @login_required. Templates mentioned here will be explained later.
        - the first function is the index function. This function basically returns base.html as known as the home page.
        - task_list and category_list function will return the task_list.html/category_list and pass to it all tasks/categoreis that are related to the current user. 
        - task_detail/category_detail will work when the user clicks on a specific task/category. This will render that specific task/category information to the user.
        - The task_create/category_create function, if the method is POST, it will receive the information that the user submited via the TaskForm/CategoryForm, will save it as a new task/category just added, and then will redirect the user to the task_list/category_list page, passing the parameters all tasks/categories (that now includes the new task just added).
        - task_update/category_update is a function that will work when the user clicks on task_detail/category_detail and on the button edit. It will render againg the TaskForm/CategoryForm, but, this time the form will be prepopulated with the info that task/category already contains. Once the user edits the form he will click on save. When the user saves the edit, the task_update/category_update view will save the new information for that specific task and will render the task_list/category_list page for the user. This function will also use json.loads to prefill the form for the user.
        - task_delete/category_delete is also a view function that can be accessed via the task_detail/category_detail view (when you click delete button). This view is very simple it wil only render the task_delete.html/category_delete.html and once you confirm by clicking delete button again, this view function will delete the task/category from the database.
        -- Notice how the views functions for categories and tasks are very similir, this is because I worked with two models but I wanted them to have the same functionality. Wanted to simplify as much as possible from the app, so I used the same mechanics, more user-friendly
    In models.py we have two models and two forms in addition to the user model (one form for each model). The model category will have a user(related to model user) a name(title) and a description. The model for task will also have a user(related to the user model), will have a title, a description, a category (related to categories model), a due_date and a boolean field called completed. For the forms we have one form for each model (except for the user model), each form will have its model, for each field in each form will be all of the models distinct parameters(title, description etc..), in each form we will also have a widget that will set the user parameter in the form as a hidden input so that it automatically sets the user property to the current user.

    All the CSS and the javascript are on the templates files. The only part there is js on this project is on the task_detail.html. The js there is used so that the user can mark a task as completed or incompleted without having to ask the server and refresh the page. This part is done with json request that goes to the task_complete function in views.py. 

    All templates for the tasks pages are very similar to the categories.
        - in task_list.html/categories_list.html it will render all tasks/categories related to the user.
        - task_detail.html/category_detaill.html will render the details for the specific task/category the user clicked on, there will be 2 buttons, one to edit and one to delete it (despite the button to mark as completed in task_detail.html that works with js).
            - task_delete.html/category_delete.html will render the delete function for the specific category/taks
            - task_update.html/category_update.html will render the respective form so that the user can update those two info.
        - task_create.html/category_create.html will render the respective form so that the userr can fill it and create a new task/category.

    In addition to that we have other less important files such as urls.py, admin.py, test.py, apps.py and etc.. 

-- How to run
    Install project dependencies by running pip install -r requirements.txt
    Make and apply migrations by running python manage.py makemigrations and python manage.py migrate.