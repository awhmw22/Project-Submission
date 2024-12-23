import socket
import tkinter as tk
from tkinter import ttk, messagebox


def request_weather(city):
    """Request weather data from the server."""
    host = '127.0.0.1'
    port = 12345

    try:
        # Connect to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        # Send city name
        client_socket.send(city.encode())

        # Receive weather data
        weather_data = client_socket.recv(4096).decode()

        client_socket.close()
        return weather_data
    except ConnectionRefusedError:
        return "Error: Could not connect to the server."
    except Exception as e:
        return f"Error: {e}"


def get_weather():
    """Handle the Get Weather button click."""
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    # Fetch weather data and update result
    weather_data = request_weather(city)
    display_weather_details(weather_data)


def display_weather_details(data):
    """Display the weather details in the text box."""
    if "Error" in data or "City not found" in data:
        result_text.config(state="normal")
        result_text.delete("1.0", "end")
        result_text.insert("1.0", data)
        result_text.config(state="disabled")
        return

    lines = data.split("\n")
    if len(lines) < 5:
        result_text.config(state="normal")
        result_text.delete("1.0", "end")
        result_text.insert("1.0", "Malformed data received.")
        result_text.config(state="disabled")
        return

    condition = lines[2].split(":")[1].strip().lower()
    condition_emoji = get_condition_emoji(condition)

    result_text.config(state="normal")
    result_text.delete("1.0", "end")

    # Add each line with appropriate styling
    result_text.insert("1.0", f"🌍 City:        {lines[0].replace('Weather in', '').strip()}\n\n", "bold")
    result_text.insert("end", f"🌡️ Temperature: {lines[1].split(':')[1].strip()}\n\n", "bold")
    result_text.insert("end", f"{condition_emoji} Condition:   {lines[2].split(':')[1].strip()}\n\n", "bold")
    result_text.insert("end", f"💧 Humidity:    {lines[3].split(':')[1].strip()}\n\n", "bold")
    result_text.insert("end", f"🌬️ Wind Speed:  {lines[4].split(':')[1].strip()}", "bold")

    result_text.config(state="disabled")


def get_condition_emoji(condition):
    """Return an emoji based on the weather condition."""
    if "clear" in condition:
        return "☀️"  # Clear sky
    elif "cloud" in condition:
        return "☁️"  # Cloudy
    elif "rain" in condition:
        return "🌧️"  # Rainy
    elif "snow" in condition:
        return "❄️"  # Snow
    elif "storm" in condition or "thunder" in condition:
        return "⛈️"  # Thunderstorm
    elif "mist" in condition or "fog" in condition:
        return "🌫️"  # Mist/Fog
    else:
        return "🌈"  # Default/Other


def on_enter(event):
    """Change button color on hover."""
    get_weather_button.config(background="#0059b3", foreground="white")


def on_leave(event):
    """Reset button color when not hovered."""
    get_weather_button.config(background="#0073e6", foreground="white")


# Tkinter GUI setup
app = tk.Tk()
app.title("Advanced Weather Client")
app.geometry("700x600")  # Larger window size
app.resizable(False, False)
app.configure(bg="#e8f4f8")  # Softer background color

# Styles
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", font=("Helvetica", 12), background="#e8f4f8")
style.configure("TFrame", background="#e8f4f8")

# Header Frame
header_frame = ttk.Frame(app)
header_frame.pack(pady=20)

header_label = ttk.Label(
    header_frame,
    text="🌤️ Advanced Weather Client 🌦️",
    font=("Helvetica", 24, "bold"),
    anchor="center",
    foreground="#003366"
)
header_label.pack()

# Input Frame
input_frame = ttk.Frame(app)
input_frame.pack(pady=10)

city_label = ttk.Label(input_frame, text="🌍 Enter City Name:")
city_label.grid(row=0, column=0, padx=5, pady=5)

city_entry = ttk.Entry(input_frame, font=("Helvetica", 14), width=30)
city_entry.grid(row=0, column=1, padx=5, pady=5)

# Styled Button with Hover Effect
get_weather_button = tk.Button(
    input_frame,
    text="Get Weather 🌤️",
    font=("Helvetica", 14, "bold"),
    background="#0073e6",
    foreground="white",
    activebackground="#004080",
    activeforeground="white",
    cursor="hand2",
    command=get_weather
)
get_weather_button.grid(row=0, column=2, padx=5, pady=5)

# Bind hover events
get_weather_button.bind("<Enter>", on_enter)
get_weather_button.bind("<Leave>", on_leave)

# Result Frame
result_frame = ttk.Frame(app)
result_frame.pack(pady=20, fill="both", expand=True)

result_label = ttk.Label(result_frame, text="📋 Weather Details:")
result_label.pack(anchor="w", padx=10, pady=5)

result_text = tk.Text(
    result_frame,
    font=("Helvetica", 12),
    height=15,
    width=70,  # Wider text box for larger dialogue area
    wrap="word",
    state="disabled",
    bg="#f8fcff",
    borderwidth=2,
    relief="groove"
)

# Configure text styles (no foreground ensures default emoji color)
result_text.tag_config("bold", font=("Helvetica", 12, "bold"))
result_text.pack(padx=10, pady=5)

# Footer
footer_label = ttk.Label(
    app,
    text="Powered by OpenWeatherMap | Developed by Abdul Waasey Huzaifa Maalik Wattoo",
    font=("Helvetica", 10, "italic"),
    anchor="center",
    foreground="#003366"
)
footer_label.pack(side="bottom", pady=10)

# Run the GUI
app.mainloop()
