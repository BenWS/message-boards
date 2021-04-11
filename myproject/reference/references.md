# References

# General
 - [Implementing Markdown as Model Function](https://simpleisbetterthancomplex.com/series/2017/10/09/a-complete-beginners-guide-to-django-part-6.html#adding-markdown)

 - Icon Finder
   - https://www.iconfinder.com/search/
 - HTML Display Property (block, inline-block, inline)
   - https://www.w3schools.com/cssref/pr_class_display.asp
 - A general guide to Flexbox
   - https://css-tricks.com/snippets/css/a-guide-to-flexbox/
 - [Python Exceptions](https://docs.python.org/3/library/exceptions.html)
 - [Python Exception Handling](https://docs.python.org/3/tutorial/errors.html)
 - [Python List Sort](https://www.w3schools.com/python/ref_list_sort.asp)
 - [Python - Convert String to Datetime](https://www.tutorialspoint.com/python/time_strptime.htm)
 - [Constructing Timezone Aware Datetime](https://docs.python.org/3/library/datetime.html#datetime.datetime.fromisoformat)
 - [Using timezone module to get timezone 'aware' date](https://docs.djangoproject.com/en/3.1/topics/i18n/timezones/#naive-and-aware-datetime-objects)
 - Django Paginator utility
    [Django Tutorial Docs](https://simpleisbetterthancomplex.com/series/2017/10/09/a-complete-beginners-guide-to-django-part-6.html#pagination)
    [Official Django Docs](https://docs.djangoproject.com/en/3.0/ref/paginator/)
 - [Background Design Resource](https://www.toptal.com/designers/subtlepatterns/)
 - [Topography Pattern](https://www.toptal.com/designers/subtlepatterns/topography/)
 - [Bootstrap Templates](https://startbootstrap.com/themes)
 - [Static File Deployment](https://docs.djangoproject.com/en/3.0/howto/static-files/deployment/)

# Django Tests
 - The test client and its methods, attributes here:
   - https://docs.djangoproject.com/en/3.0/topics/testing/tools/
 - Web application-specific test cases:
   - https://docs.djangoproject.com/en/3.1/topics/testing/tools/#assertions
 - Running Tests:
   - https://docs.djangoproject.com/en/3.0/topics/testing/overview/
 - Python unit tests module:
   - https://docs.python.org/3/library/unittest.html#classes-and-functions 

# Bootstrap

## Pagination
 - [Overview](https://getbootstrap.com/docs/4.0/components/pagination/)

## Navbar
 - Full example of Boostrap Navigation Bar w/drop-down menu example: 
   - https://getbootstrap.com/docs/4.6/components/navbar/#supported-content
   - In further detail, the above link contains information on:
     - Control on alignment of navigation elements
     - Dropdown-link elements 
 - The flexbox me-auto or ms-auto classes can be used to position elements as needed (as done in above example):
   - https://getbootstrap.com/docs/4.6/utilities/flex/#auto-margins
   
## Forms
 - 'invalid-feedback' class and Bootstrap Form validation: 
   - https://getbootstrap.com/docs/5.0/forms/validation/
 - Basic example for Bootstrap form structure: 
   - https://getbootstrap.com/docs/5.0/forms/overview/#overview
 - Bootstrap Alerts
   - https://getbootstrap.com/docs/5.0/components/alerts/
   
 # Cards
 
 - Cards Overview: 
   - https://getbootstrap.com/docs/4.0/components/card/

# Django Forms
 - Form **class** fields and methods:
   - https://docs.djangoproject.com/en/3.0/ref/forms/api/#django.forms.Form
 - Django Form class form fields: 
   - https://docs.djangoproject.com/en/3.0/topics/forms/#looping-over-the-form-s-fields
 - Building a generic form in Django:
   - https://docs.djangoproject.com/en/3.0/topics/forms/#building-a-form-in-django
- Customizing the 'clean' method:
   - https://docs.djangoproject.com/en/3.0/ref/forms/validation/#validating-fields-with-clean
- Building a model form in Django:
  - https://docs.djangoproject.com/en/3.0/topics/forms/modelforms/#django.forms.ModelForm
 - Form fields:
   - Overview: https://docs.djangoproject.com/en/3.0/topics/forms/#more-on-fields
   - In-depth: https://docs.djangoproject.com/en/3.0/ref/forms/fields/
     - As more information - contains 'fields' class methods and properties
   - Form field widgets: https://docs.djangoproject.com/en/3.0/ref/forms/widgets
     
# Django Views
 - Class-based views (general)
   - https://docs.djangoproject.com/en/3.0/topics/class-based-views/
 - Django Authentication views:
   - https://docs.djangoproject.com/en/3.1/topics/auth/default/#all-authentication-views
 - Django Generic Editing Views:
   - https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-editing/
 - [Basic Example of a Class-Based View Implementation](https://simpleisbetterthancomplex.com/series/2017/10/09/a-complete-beginners-guide-to-django-part-6.html#class-based-view)
 - [Basic Example of a Generic Class-Based View Implementation](https://simpleisbetterthancomplex.com/series/2017/10/09/a-complete-beginners-guide-to-django-part-6.html#generic-class-based-view)
 - [Django Documentation for Generic-Editing Views](https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-editing/)
 - [Function-based View Decorators](https://docs.djangoproject.com/en/3.0/topics/http/decorators/)
 - [Class-based View Decorators](https://docs.djangoproject.com/en/3.0/topics/class-based-views/intro/#id1)
 - [Generic Class-Based View Reference](https://ccbv.co.uk/)
   
 # Django Models
 - Django Shell Queries
   - https://docs.djangoproject.com/en/3.0/topics/db/queries/
 - Django Model Query Aggregations
   - https://docs.djangoproject.com/en/3.0/topics/db/aggregation/
 - Common Aggregations
   - https://docs.djangoproject.com/en/3.0/topics/db/aggregation/#cheat-sheet

# Django User Authentication Modules
  - User authentication: 
    - https://docs.djangoproject.com/en/3.0/topics/auth/
  
# Django Templates
- [Template Inheritence](https://docs.djangoproject.com/en/3.0/ref/templates/language/#template-inheritance)
- ['include' Tag](https://docs.djangoproject.com/en/3.0/ref/templates/builtins/#std:templatetag-include) 
- [Django Built-in Template Tags](https://docs.djangoproject.com/en/3.0/ref/templates/builtins/)
- For Loop: https://docs.djangoproject.com/en/3.0/ref/templates/builtins/#for
 - [Custom Template Tags](https://docs.djangoproject.com/en/3.1/howto/custom-template-tags/#writing-custom-template-tags)
 - [Custom Template Tag Filters](https://docs.djangoproject.com/en/3.1/howto/custom-template-tags/#writing-custom-template-filters)
   - Tutorial: https://simpleisbetterthancomplex.com/series/2017/09/25/a-complete-beginners-guide-to-django-part-4.html#creating-custom-template-tags
 - Date template filter:
   - https://docs.djangoproject.com/en/3.0/ref/templates/builtins/#date 
   
# Email Backend:
 - Various email backends and configuration options available in Django:
   - https://docs.djangoproject.com/en/3.0/topics/email/

# URL Configuration:
 - Short Django guide to using regex in URL patterns:
   - https://docs.djangoproject.com/en/3.0/topics/http/urls/#using-regular-expressions
 - List of common regex patterns:
   - Short List: https://simpleisbetterthancomplex.com/series/2017/09/18/a-complete-beginners-guide-to-django-part-3.html#list-of-useful-url-patterns
   - More comprehensive list: https://simpleisbetterthancomplex.com/references/2016/10/10/url-patterns.html
   - URL Resolvers: https://docs.djangoproject.com/en/3.0/ref/urlresolvers/#django.urls.reverse
   
 