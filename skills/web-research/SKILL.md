---
name: web-research
description: Fetch public web pages, cite them, and label every figure as read, estimate or unverified. Use for any research, price, rating, part-number, funding or regulation question.
---

# Web research

Do not give facts from memory as if you read them. Each fact gets a source
that you read in this task, or a label that says it has no source.

## Fetch a page

```sh
curl -sL -m 20 -A "Mozilla/5.0" "<url>" -o page.html -w '%{http_code}\n'
sed 's/<[^>]*>/ /g' page.html | tr -s ' \n' | grep -i -n '<keyword>' | head
```

- Prefer primary sources: the standard, the law, the datasheet, the
  manufacturer, the official register.
- Static HTML pages work. Many shops send only JavaScript, and the text
  that you get is empty. If the text is empty, record the site as not
  readable.
- If the HTTP code is `000` or the site blocks you, record that. Do not
  retry through a proxy, a cache, a translator or another host.
- If a search engine gives no usable result, go to the primary sources.

## Budget

- Make 3 or fewer fetch attempts for each item.
- When the budget for an item is spent, label the item and continue.
- Write the result when the items are complete. Do not continue to search
  for a better source without end.

## Labels

Give each figure one label:

- **[read]**: The figure is in text that you fetched in this task. Give the
  full URL and the date that you read it. Do not round the figure more than
  the page does.
- **[estimate]**: The figure comes from memory, a conversion or your own
  reasoning. Tell how you got it.
- **[unverified]**: You could not open the source. If the task asks for the
  item, list it without figures. Do not remove a required item because its
  site is blocked.

## Part numbers and ratings

- Write a part number, an order code or a rating only from a source that
  you read. Give the URL and the date.
- If you could not read a source, leave the field blank and write
  "to verify". A blank field is better than a guess.

## Write the result

- Quote the caveats that the page gives: sale banners, "from" prices,
  proposed changes, dates of application.
- Record the URL and the date for each fact.
- End with a **Sources** list of URLs.
- Add one line that names the sources that you could not open.
