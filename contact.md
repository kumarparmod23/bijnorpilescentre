---
layout: default
title: Contact & Book Consultation — Bijnor Piles Centre
permalink: /contact/
description: Book a consultation at Bijnor Piles Centre — call, WhatsApp or visit our clinic in Bijnor, Uttar Pradesh.
---

<section class="bg-gradient-to-br from-primary to-primary-dark text-white">
  <div class="max-w-5xl mx-auto px-4 py-14 md:py-20">
    <div class="text-accent font-semibold text-xs uppercase tracking-widest mb-3">Get In Touch</div>
    <h1 class="font-serif text-4xl md:text-5xl font-bold mb-4">Book Your Consultation</h1>
    <p class="text-lg opacity-90 max-w-2xl">Speak to us in complete confidence. We'll guide you through your treatment options and answer every question.</p>
  </div>
</section>

<section class="py-14 md:py-20">
  <div class="max-w-5xl mx-auto px-4 grid md:grid-cols-2 gap-8">
    <div class="bg-white rounded-2xl border border-slate-100 shadow-sm p-8">
      <h2 class="font-serif text-2xl font-bold text-primary mb-6">Clinic Details</h2>
      <div class="space-y-5 text-slate-700">
        <div class="flex gap-4">
          <div class="w-11 h-11 rounded-lg bg-accent/10 text-accent flex items-center justify-center text-xl flex-shrink-0">📍</div>
          <div>
            <div class="text-xs uppercase tracking-wide text-slate-500 font-semibold">Address</div>
            <div>Bijnor, Uttar Pradesh, India</div>
          </div>
        </div>
        <div class="flex gap-4">
          <div class="w-11 h-11 rounded-lg bg-accent/10 text-accent flex items-center justify-center text-xl flex-shrink-0">📞</div>
          <div>
            <div class="text-xs uppercase tracking-wide text-slate-500 font-semibold">Phone</div>
            <a href="tel:{{ site.clinic.phone }}" class="hover:text-accent">{{ site.clinic.phone }}</a>
          </div>
        </div>
        <div class="flex gap-4">
          <div class="w-11 h-11 rounded-lg bg-accent/10 text-accent flex items-center justify-center text-xl flex-shrink-0">💬</div>
          <div>
            <div class="text-xs uppercase tracking-wide text-slate-500 font-semibold">WhatsApp</div>
            <a href="https://wa.me/{{ site.clinic.whatsapp | remove: '+' | remove: '-' }}" class="hover:text-accent">Chat with us</a>
          </div>
        </div>
        <div class="flex gap-4">
          <div class="w-11 h-11 rounded-lg bg-accent/10 text-accent flex items-center justify-center text-xl flex-shrink-0">🕒</div>
          <div>
            <div class="text-xs uppercase tracking-wide text-slate-500 font-semibold">Hours</div>
            <div>Mon – Sat: 10:00 AM – 7:00 PM<br>Sunday: By appointment</div>
          </div>
        </div>
      </div>
    </div>

    <div class="bg-gradient-to-br from-primary to-primary-dark text-white rounded-2xl shadow-lg p-8">
      <h2 class="font-serif text-2xl font-bold mb-3">Why Visit Us</h2>
      <ul class="space-y-3 text-sm opacity-95 mb-7">
        <li class="flex gap-3"><span class="text-accent">●</span> Free first evaluation</li>
        <li class="flex gap-3"><span class="text-accent">●</span> Painless, day-care procedures</li>
        <li class="flex gap-3"><span class="text-accent">●</span> 100% confidential consultation</li>
        <li class="flex gap-3"><span class="text-accent">●</span> Most treatments under 30 minutes</li>
        <li class="flex gap-3"><span class="text-accent">●</span> Transparent, affordable pricing</li>
      </ul>
      <div class="space-y-3">
        <a href="tel:{{ site.clinic.phone }}" class="block bg-accent hover:bg-accent-dark text-white text-center py-3.5 rounded-lg font-semibold transition">📞 Call Now</a>
        <a href="https://wa.me/{{ site.clinic.whatsapp | remove: '+' | remove: '-' }}" class="block bg-green-500 hover:bg-green-600 text-white text-center py-3.5 rounded-lg font-semibold transition">💬 WhatsApp Us</a>
      </div>
    </div>
  </div>
</section>

<script type="application/ld+json">
{
  "@context":"https://schema.org",
  "@type":"MedicalBusiness",
  "name":"Bijnor Piles Centre",
  "address":{"@type":"PostalAddress","addressLocality":"Bijnor","addressRegion":"UP","addressCountry":"IN"},
  "telephone":"{{ site.clinic.phone }}",
  "medicalSpecialty":"Proctology",
  "openingHours":"Mo-Sa 10:00-19:00"
}
</script>
