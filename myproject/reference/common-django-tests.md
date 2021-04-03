# View Tests
 - URL resolves to the correct function?
 - Response Status Codes?
   - 200 for page visits
   - 302 for form submissions
   - 404 for invalid resource specified (if view relies on URL parameters)
   - Generally - unauthorized unauthenticated users cannot access pages or take particular actions, as designed
 - If view contains form:
   - Does the view even contain the form, and is it the correct form?
   - Form field contains expected number of types of fields
   - Form contains csrf_token   

# Form Submission Tests
 - Valid form submission
   - Status code of 302
   - Redirects to the expected destination
   - Does the form submission affect the environment as expected? E.g. if the purpose of the form to create a user, is a user created? 
   
 - Invalid form submission
   - Form contains error
   - Status code of 200
   - Are form's actions prevented from moving forward? I.e. if the purpose of the form is to create a new user, is the new user *prevented* from being created for a form submission.
   - (**check that users are created** as needed for form submission tests ) 

# Form *Object* Tests
 - Form fields are in expected sequence 
  