---
title: "Contact Us"
date: 2025-05-21T09:00:00+03:00 # Adjust date as needed
layout: "single" # Or "page" or similar, depending on your theme's layouts
url: "/contact/" # Ensure this is the URL you want
outputs:
  - HTML
---

## Get in Touch

Have questions, feedback, or just want to say hello? Use the form below to send us a message!

<form name="contact" method="POST" data-netlify="true" netlify-honeypot="bot-field">
    <input type="hidden" name="form-name" value="contact" />
    <p style="display:none;">
        <label>Don’t fill this out if you’re human: <input name="bot-field" /></label>
    </p>
    <p>
        <label for="email">Your Email:</label>
        <input type="email" name="email" id="email" required>
    </p>
    <p>
        <label for="message">Message:</label>
        <textarea name="message" id="message" rows="6" required></textarea>
    </p>
    <p>
        <button type="submit">Send Message</button>
    </p>
</form>

---