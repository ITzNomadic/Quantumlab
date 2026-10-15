# Security Policy

QuantumLab is an early-stage local desktop educational application.

**Important:** its symbolic expression parser currently calls `sympy.sympify()` on user-supplied text. It is not suitable for processing untrusted expressions. Do not embed the parser into a public web API or service without a secure parsing redesign.

For a suspected vulnerability, avoid posting exploit payloads or sensitive details in a public issue. Contact the maintainer privately using GitHub's available profile contact details, or open a non-sensitive issue requesting a private channel.

Supported security fixes are targeted at the latest version on the default branch.
