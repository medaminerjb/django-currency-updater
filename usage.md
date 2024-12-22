{% load currency_tags %}

<h1>Currency Rates</h1>
<p>USD Rate: {% get_currency_rate "USD" %}</p>
<p>EUR Rate: {% get_currency_rate "EUR" %}</p>

<h2>Formatted Prices</h2>
<p>Price in USD: {{ 1234.56|format_currency:"USD" }}</p>
<p>Price in EUR: {{ 1234.56|format_currency:"EUR" }}</p>
