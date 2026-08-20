# Product Upload Agent

An AI-assisted product upload agent that prepares product listing information from product images.

The agent is designed for a retail e-commerce workflow where an admin takes product photos, selects one or more images, and uses the agent to automatically research and prepare the product information needed for a product upload form.

The agent does not create or manage products itself. Its responsibility is to analyze product images, research the identified products, and return structured product drafts that an administrator can review and complete.

---

## 1. Project Purpose

The Product Upload Agent was built to reduce the repetitive work involved in uploading products to a retail website.

The current manual workflow requires an admin to:

1. Take a product photo.
2. Open the retail website's admin dashboard.
3. Open the product upload form.
4. Use a visual search tool such as Google Lens to identify the product.
5. Read the information returned by the search.
6. Move back to the admin website.
7. Enter the product name.
8. Write a short description.
9. Write a full description.
10. Manually enter business-specific information such as:
    - Category
    - Price
    - Stock quantity
    - Availability
    - Featured status

This becomes repetitive when uploading many products.

The Product Upload Agent is intended to remove the research and writing portion of this process.

Instead of repeatedly switching between applications, the admin will eventually be able to select multiple product images from the retail website and send them to the agent.

The agent will process the images one at a time and return product drafts.

The admin will then review the generated information and manually complete the business-specific fields.

---

# 2. Core Responsibility

The agent is responsible for:

- Understanding a product image
- Reading visible product labels and packaging
- Identifying the likely:
  - Brand
  - Product name
  - Model number
  - Product type
  - Variant
  - Specifications
- Creating a useful search query
- Searching the web for supporting product information
- Combining visual evidence and web research
- Generating:
  - Product name
  - Short description
  - Full description
- Providing a confidence score
- Providing research sources
- Returning a structured product draft

The agent is NOT responsible for:

- Setting product prices
- Determining stock quantity
- Determining business availability
- Deciding whether a product is featured
- Creating the final product record
- Uploading the final product image to Amazon S3
- Writing product records to Firestore
- Managing the retail website
- Automatically publishing products

These responsibilities remain with the administrator and the existing retail website.

---

# 3. Important Architecture Decision

The product image originates from the administrator's phone or computer.

The image does NOT initially exist in Amazon S3.

The current retail website workflow uploads the image to Amazon S3 only when the administrator completes and submits the product form.

Therefore, Amazon S3 is NOT an input source for the Product Upload Agent.

The future workflow is:

```text
Admin's Phone / Computer
        |
        | Select product image(s)
        v
Retail Website
        |
        | Send selected image files
        v
Product Upload Agent API
        |
        v
Image Analysis
        |
        v
Product Identification
        |
        v
Web Research
        |
        v
Product Draft Generation
        |
        v
API Response
        |
        v
Retail Website
        |
        | Display incomplete product forms
        v
Admin Review
        |
        | Complete business fields
        v
Save Product
        |
        +--------------------+
        |                    |
        v                    v
     Amazon S3           Firestore
     Image Storage       Product Data