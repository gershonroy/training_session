import tkinter as tk
from tkinter import messagebox
import requests
import json
from PIL import Image, ImageTk  # Import Pillow

current_access_token = None

def login():
    """
    Handles the login process when the user clicks the login button.
    """
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Error", "Username and password are required.")
        return

    # FastAPI endpoint URL for login (the /token endpoint)
    token_url = "https://127.0.0.1:8000/token"  # Or the correct address

    # Data to send in the request body (form data)
    payload = {
        "grant_type": "password",
        "username": username,
        "password": password,
    }

    try:
        # Make the POST request to the /token endpoint (disable SSL verification)
        response = requests.post(token_url, data=payload, verify=False) # added verify=False

        # Check the response status code
        if response.status_code == 200:
            # Parse the JSON response to get the access token
            token_data = response.json()
            access_token = token_data.get("access_token")

            if access_token:
                messagebox.showinfo("Success", "Login successful!")
                #  You can now store the access_token and use it for other requests
                #  For example, to get user data from /users/me:
                # user_me_url = "https://127.0.0.1:8000/users/me"
                # headers = {"Authorization": f"Bearer {access_token}"}
                # user_me_response = requests.get(user_me_url, headers=headers, verify=False)
                # if user_me_response.status_code == 200:
                #     user_data = user_me_response.json()
                #     print(user_data) #do something with user data.
                # else:
                #    messagebox.showerror("Error", f"Failed to get user data: {user_me_response.text}")

            else:
                messagebox.showerror("Error", "Access token not found in response.")
        else:
            # Display an error message with the server's response
            error_message = f"Login failed: {response.status_code} - {response.text}"
            messagebox.showerror("Error", error_message)
    except requests.exceptions.RequestException as e:
        # Handle network errors (e.g., connection refused, timeout)
        messagebox.showerror("Error", f"Connection error: {e}")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Invalid JSON response from server.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def show_signup_form():
    """
    Displays the sign-up form with additional fields.
    """
    # Clear the initial login form
    username_label.grid_forget()
    password_label.grid_forget()
    username_entry.grid_forget()
    password_entry.grid_forget()
    login_button.grid_forget()
    signup_button.grid_forget()

    # Pack the sign-up form elements using grid
    global first_name_label, first_name_entry, last_name_label, last_name_entry, username_label_signup, username_entry_signup, password_label_signup, password_entry_signup, signup_button_final
    first_name_label = tk.Label(root, text="First Name:")
    first_name_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    first_name_entry = tk.Entry()
    first_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    last_name_label = tk.Label(root, text="Last Name:")
    last_name_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    last_name_entry = tk.Entry()
    last_name_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    username_label_signup = tk.Label(root, text="Set Username:")
    username_label_signup.grid(row=3, column=0, padx=10, pady=5, sticky="e")
    username_entry_signup = tk.Entry()
    username_entry_signup.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    password_label_signup = tk.Label(root, text="Set Password:")
    password_label_signup.grid(row=4, column=0, padx=10, pady=5, sticky="e")
    password_entry_signup = tk.Entry(show="*")
    password_entry_signup.grid(row=4, column=1, padx=10, pady=5, sticky="w")

    signup_button_final = tk.Button(root, text="Sign Up", command=signup)
    signup_button_final.grid(row=5, column=0, columnspan=2, pady=10)

def signup():
    """
    Handles the sign-up process when the user clicks the sign-up button in the sign-up form.
    """
    username = username_entry_signup.get()
    password = password_entry_signup.get()
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()

    if not username or not password or not first_name or not last_name:
        messagebox.showerror("Error", "All fields are required for sign up.")
        return

    # FastAPI endpoint URL for sign up
    signup_url = "https://127.0.0.1:8000/signup"  # Or the correct address

    # Data to send in the request body (JSON data)
    payload = {
        "username": username,
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
    }

    try:
        # Make the POST request to the /signup endpoint (disable SSL verification)
        response = requests.post(signup_url, json=payload, verify=False) # Changed data to json, added verify=False

        # Check the response status code
        if response.status_code == 201:
            messagebox.showinfo("Success", "Sign up successful! You can now log in.")
            # Clear the form for the user to log in
            username_entry_signup.delete(0, tk.END)
            password_entry_signup.delete(0, tk.END)
            first_name_entry.delete(0, tk.END)
            last_name_entry.delete(0, tk.END)
            show_login_form() #show login form
        else:
            # Display an error message with the server's response
            error_message = f"Sign up failed: {response.status_code} - {response.text}"
            messagebox.showerror("Error", error_message)
    except requests.exceptions.RequestException as e:
        # Handle network errors (e.g., connection refused, timeout)
        messagebox.showerror("Error", f"Connection error: {e}")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Invalid JSON response from server.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def show_login_form():
    """
    Display the login form
    """
    # Clear the signup form
    if hasattr(root, 'first_name_label'):
        first_name_label.grid_forget()
        first_name_entry.grid_forget()
        last_name_label.grid_forget()
        last_name_entry.grid_forget()
        username_label_signup.grid_forget()
        username_entry_signup.grid_forget()
        password_label_signup.grid_forget()
        password_entry_signup.grid_forget()
        signup_button_final.grid_forget()

    # Restore the login form using grid
    username_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    username_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
    password_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    password_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
    login_button.grid(row=3, column=0, columnspan=2, pady=10)
    signup_button.grid(row=4, column=0, columnspan=2, pady=5)

# Create the main window
root = tk.Tk()
root.title("Login page")

# Set the geometry (width x height)
root.geometry("500x500")  # Adjusted size

# Configure grid layout for centering
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(5, weight=1) # Adjust based on the last row

# Load the background image
try:
    bg_image = Image.open("/Users/gershonroy/Downloads/bg1.png")  # Replace with your image file
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Create a label to display the background image
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)  # Cover the entire window
except FileNotFoundError:
    print("Error: background.png not found. Using default background color.")
    root.config(bg="lightblue")  # Default background color

# Create labels and entry fields for username and password using grid
username_label = tk.Label(root, text="Username:")
username_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
username_entry = tk.Entry()
username_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
password_label = tk.Label(root, text="Password:")
password_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
password_entry = tk.Entry(root, show="*")  # Use show="*" to hide the password
password_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

# Create a login button using grid
login_button = tk.Button(root, text="Login", command=login)
login_button.grid(row=3, column=0, columnspan=2, pady=10)

# Create a sign-up button using grid
signup_button = tk.Button(root, text="Sign Up", command=show_signup_form)
signup_button.grid(row=4, column=0, columnspan=2, pady=5)

# Run the Tkinter event loop
root.mainloop()



