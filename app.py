from flask import Flask, render_template, request
from secret_sharing import make_shares, reconstruct_secret
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    shares = []
    reconstructed = None
    secret = None

    if request.method == 'POST':
        try:
            secret = int(request.form['secret'])
            total = int(request.form['total'])
            threshold = int(request.form['threshold'])

            shares = make_shares(secret, threshold, total)

            # Reconstruct from first k shares
            selected = shares[:threshold]
            reconstructed = reconstruct_secret(selected)

            # Plot
            x_vals = [s[0] for s in shares]
            y_vals = [s[1] for s in shares]
            plt.figure()
            plt.scatter(x_vals, y_vals, color='blue')
            plt.title('Shamir Secret Sharing')
            plt.xlabel('Share Index')
            plt.ylabel('Share Value')
            plt.grid(True)
            plt.savefig('static/chart.png')
            plt.close()

        except Exception as e:
            return f"Error: {e}"

    return render_template('index.html', shares=shares, reconstructed=reconstructed, secret=secret)

if __name__ == '__main__':
    app.run(debug=True)
