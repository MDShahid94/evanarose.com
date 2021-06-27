---
title: একটি সাধারন C++ প্রোগ্রাম
sidebar: cpp_sidebar
permalink: cpp-ch1-a_simple_cpp_program.html
folder: cpp
customjs: /js/tooltips.js
---

## প্রোগ্রাম ১.১ - একটি স্ট্রিং প্রিন্ট করা

আসুন আমরা C++ প্রোগ্রামের একটি সাধারণ উদাহরণ দিয়ে শুরু করি যা স্ক্রিনে একটি <a href="#" onClick="return false;" data-toggle="tooltip" data-original-title="{{site.data.glossary.string}}">string</a> প্রিন্ট করে।

```cpp
#include <iostream> // include header file
using namespace std;

int main()
{
cout << "C++ is better than C.\n"; // C++ statement
return 0;
} // End of example
```
এই সাধারণ প্রোগ্রামটি বেশ কয়েকটি C++ বৈশিষ্ট্য প্রদর্শন করে। 

## প্রোগ্রাম বৈশিষ্ট্য

C এর মতো, C++ প্রোগ্রাম হ'ল <a href="#" onClick="return false;" data-toggle="tooltip" data-original-title="{{site.data.glossary.function}}">function</a> গুলির সংকলন। উপরের উদাহরণে কেবলমাত্র একটি ফাংশন রয়েছে `main()`। যথারীতি প্রোগ্রামটির নির্বাহ `main()` থেকে শুরু হয়। প্রতিটি C++ প্রোগ্রামের অবশ্যই একটি `main()` থাকতে হবে। C++ একটি Free Form (গঠন মুক্ত) ভাষা। কয়েকটি ব্যতিক্রম ছাড়া, <a href="#" onClick="return false;" data-toggle="tooltip" data-original-title="{{site.data.glossary.compiler}}">compiler</a> carriage return এবং white space গুলিকে উপেক্ষা করে। C এর মতো, C++ <a href="#" onClick="return false;" data-toggle="tooltip" data-original-title="{{site.data.glossary.statement}}">statement</a> গুলি সেমিকোলনের (`;`) সাথে শেষ হয়।

### Comments (মন্তব্য)

C++ এ Comments (মন্তব্যগুলি) নির্দেশিত করতে `//` (ডাবল স্ল্যাশ) প্রতীকটি ব্যবহার করা হয়। মন্তব্যগুলি ডাবল স্ল্যাশ প্রতীক দিয়ে শুরু হয় এবং লাইনের শেষে শেষ হয়। একটি Comment (মন্তব্য) লাইনের যে কোনও জায়গায় শুরু হতে পারে এবং লাইনটির শেষ অবধি যা কিছু অনুসৃত হয় তা উপেক্ষা করে কমেন্ট হিসেবে নির্ধারণ করে। মনে রাখবেন যে এখানে কমেন্টের কোনও সমাপ্তি চিহ্ন নেই।
ডাবল স্ল্যাশ (//) যুক্ত Comment গুলি মূলত একটি একক লাইনের মন্তব্য। একাধিক লাইনের কমেন্ট লিখতে এভাবে লেখা যেতে পারে:
```
// This is an example of 
// C++ program to illustrate 
// Some of its features
```
C এর / *, * / মন্তব্য প্রতীকটি (comment symbol) এখানেও বৈধ এবং একাধিক লাইনের মন্তব্যের জন্য অধিক উপযুক্ত। নিম্নলিখিত Comment টি অনুমোদিত:
```
/* This is an example of 
    C++ program to illustrate 
    some of its features
*/
```
আমরা আমাদের প্রোগ্রামগুলিতে যেকোনো একটি বা উভয় স্টাইল ব্যবহার করতে পারি। যেহেতু এটি C++ টিউটোরিয়াল তাই আমরা কেবল C++ স্টাইল ব্যবহার করব। তবে মনে রাখবেন যে আমরা কোনও প্রোগ্রাম লাইনের মধ্যে `//` স্টাইলের comment ঢোকাতে পারি না। উদাহরণস্বরূপ, নীচের উদাহরণে ডাবল স্ল্যাশ Comment ব্যবহার করা যাবে না:
```cpp
for(j=0; j<n; /* loops n times */ j++)
```

### Output Operator

প্রোগ্রাম ১.১-এর একমাত্র Statement টি হলো, একটি আউটপুট Statement।
```cpp
cout << "C++ is better than C.\n";
```
এই statement টি উদ্ধৃতি চিহ্নের (`" "`) ভেতরের স্ট্রিং-টিকে (`C++ is better than C.\n`) স্ক্রিনে প্রদর্শিত করে। এই Statement টিতে দুটি নতুন C++ বৈশিষ্ট্য, `cout` এবং `<<` -এর পরিচয় দেওয়া হয়েছে। `cout` ('C আউট' হিসাবে উচ্চারিত) <a href="#" onClick="return false;" data-toggle="tooltip" data-original-title="{{site.data.glossary.identifier}}">identifier</a> টি একটি পূর্বনির্ধারিত object যা C++ এর Standard output stream -কে উপস্থাপন করে। 
এখানে, Standard output stream বলতে ডিসপ্লে স্ক্রিন। তবে অন্য যেকোনো আউটপুট ডিভাইসে এর পুনর্নির্দেশ করা সম্ভব। আমরা পরে স্ট্রিমগুলি বিস্তারিত আলোচনা করব।

অপারেটর `<<` কে `insertion` বা `put to` অপারেটরে বলা হয়। এটি ডান পাশের ভেরিয়েবলের content টিকে বাম পাশের object -এ সন্নিবেশ করায় বা প্রেরণ করে (চিত্র ১.১)।

{% include image.html file="cpp_1-1.png" alt="Output using insertion operator" caption="চিত্র ১.১ Insertion Operator -এর মাধ্যমে স্ক্রিনে আউটপুট প্রদর্শন" %}

<span class="basketball" data-toggle="popover">Basketball</span>

{% include links.html %}
