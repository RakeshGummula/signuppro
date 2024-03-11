from django.forms import model_to_dict
from django.shortcuts import render,redirect
from loginapp.models import Patient, Doctor
from django.http import HttpResponse

def Dashboardpage(request):
    if 'username' not in request.session:
        return redirect('login')

    username = request.session['username']

    try:
        patient = Patient.objects.get(username=username)
        user_data = model_to_dict(patient)
        user_data['is_patient'] = True
    except Patient.DoesNotExist:
        try:
            doctor = Doctor.objects.get(username=username)
            user_data = model_to_dict(doctor)
            user_data['is_doctor'] = True
        except Doctor.DoesNotExist:
            return HttpResponse("User not found")

    return render(request, "Dashboard.html", {'user_data': user_data})

def SignupPage(request):
    if request.method == "POST":
        uname = request.POST['username']
        email = request.POST['email']
        role = request.POST['role']

        # Checking if the username or email is already registered for either patients or doctors
        if Patient.objects.filter(username=uname).exists() or Patient.objects.filter(email=email).exists() or Doctor.objects.filter(username=uname).exists() or Doctor.objects.filter(email=email).exists():
            error_message = "Username or email id is already registered."
            return render(request, "Signup.html", {'error_message': error_message})

        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            error_message = "Your password and confirm password are mismatched."
            return render(request, "Signup.html", {'error_message': error_message})

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        address_line1 = request.POST['address_line1']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']

        # Handle the uploaded profile picture
        profile_picture = request.FILES.get('profile_picture')

        # Additional fields for Patient and Doctor
        if role == 'patient':
            user = Patient(username=uname, email=email, password=password, first_name=first_name, last_name=last_name, address_line1=address_line1, city=city, state=state, pincode=pincode, profile_picture=profile_picture)
        elif role == 'doctor':
            user = Doctor(username=uname, email=email, password=password, first_name=first_name, last_name=last_name, address_line1=address_line1, city=city, state=state, pincode=pincode, profile_picture=profile_picture)
        else:
            error_message = "Invalid role selected."
            return render(request, "Signup.html", {'error_message': error_message})

        # Save the user to the database
        user.save()

        return redirect('login')

    return render(request, "Signup.html")

def LoginPage(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            # Check if the user is a patient
            user = Patient.objects.get(username=username, password=password)
        except Patient.DoesNotExist:
            try:
                # Check if the user is a doctor
                user = Doctor.objects.get(username=username, password=password)
            except Doctor.DoesNotExist:
                # User not found, or invalid credentials
                return render(request, "Login.html", {'error_message': 'Invalid username or password'})

        # If the user is found, set the username in the session and redirect to the dashboard
        request.session['username'] = user.username
        return redirect('dashboard')

    return render(request, "Login.html")

def Logout(request):
    if 'username' in request.session:
        del request.session['username']
    return redirect('login')