# Signals

Show students how to react to events

## What are the objectives?

- Understand how to create signals
- Understand why it is necessary to add the signal import in `apps.py`
- Understand on a high level how each signal works
- Understand when to use signals

## Pre-requisites

1. Clone this repo.
2. Create a virtual environment.
3. Install the deps using `pip install -r requirements/dev.lock`.
4. Run the migrations using `./manage.py migrate`.
5. Create a super user using `./manage.py createsuperuser`.

## Steps

## Create Signal

Explain that sometimes you want your app to react to certain "events". For example, we want to create an associated `Employee` each time a user that is created with `is_employee=True`.

1. Create a `signals.py` inside of `employees`.
2. Create a function called `create_employee` and decorate it with a `post_save` signal, and have the sender be `User`.
   - **Note:** import `get_user_model` from `django.contrib.auth` and set `User = get_user_model()`), and avoid importing the custom user model directly (explain that this is good practice, should the user model change the code here won't).
3. Check if the `user` instance has been created in the body of `create_employee` and if `is_employee` is `True`.
4. Create an employee associated with the `user` instance (keep department as `None`).
5. Demo this in the admin panel and show them that it doesn't work!
   - Explain that just creating this file doesn't do anything. We need to let Django discover this file somehow and that naming it `signals.py` is just a convention.
6. Go to `apps.py` and add a `ready` method to `EmployeesConfig` and add an import to `employees.signals` in that method.
7. Now demo the signal working in the admin panel.
   - Create a user with `is_employee` enabled and show them that an `Employee` has been created.

## Sync Signal

Explain that `post_save` signal is good for operations that can be made after the object has been saved. If we need to do some action based on whether a value has changed or not, then we must use a `pre_save` signal. For example, we want to react to `is_employee` changing and ensure that an associated `Employee` object is created/deleted depending on its value.

1. Create a `sync_employee` function and decorate it with a `pre_save` signal, have the sender be `User`.
2. Check if the `instance` has a `pk` (e.g., `if instance.pk:`).
   - This is how we can check if the instance has been created or not. If `pk` exists it means that this instance is being updated.
3. Fetch the `user` from the database and compare the `is_employee` value from the database compared with the value on the instance prior to saving.
   - Emphasize that the instance will be different than the `user` in the database because it still hasn't been saved (this is only possible in a `pre_*` signal).
4. If the `is_employee` has changed from `True` to `False` then delete the `Employee` associated with the user instance.
5. If the `is_employee` has changed from `False` to `True` then create an `Employee` associated with the `user` instance.
6. Now demo the signal working in the admin panel.
   - Disable a user with `is_employee=True` and show them that the related `Employee` has been deleted (vice-versa).

Explain that while this works and that they can do many things with signals that they should use them sparingly. Having a database hit while saving an object is heavy, and can slow down the app. There are other ways to go about this, but if they are trying to react to 3rd party Django app behavior and/or have a consistent behavior accross the app that they can do this.
