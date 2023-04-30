"""
    How to run

    Install the REA module by entering the below line into Terminal:
    pip install .\src\rea

    Run the script by entering the below line into Terminal:
    py.exe .\main.py
"""


from concurrent.futures import ThreadPoolExecutor, wait
from csv import DictWriter
from typing import List


from realestate_com_au import RealestateComAu
from realestate_com_au.objects.listing import Listing

client = RealestateComAu()

final_listings = []


def dict_from_listing(listing: Listing):
    listing_dict = {
        "Short Address": listing.short_address,
        "Full Address": listing.full_address,
        "Sale Price (Text)": listing.price_text
        if listing.price_text is not None
        else "UNK",
        "Sale Price (Number)": f"${listing.price}"
        if listing.price is not None
        else "UNK",
        "Land Size": listing.land_size,
        "Bedrooms": listing.bedrooms,
        "Bathrooms": listing.bathrooms,
        "Sale Date": listing.sold_date,
    }

    final_listings.append(listing_dict)


def run(listings: List[Listing], location: str):
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(dict_from_listing, listing) for listing in listings]
        wait(futures)

        location_name = location.replace(" ", "").strip().lower()
        with open(f"{location_name}.csv", "w", newline="") as output_file:
            dict_writer = DictWriter(
                output_file,
                [
                    "Short Address",
                    "Full Address",
                    "Sale Price (Text)",
                    "Sale Price (Number)",
                    "Land Size",
                    "Bedrooms",
                    "Bathrooms",
                    "Sale Date",
                ],
            )
            dict_writer.writeheader()
            dict_writer.writerows(final_listings)


if __name__ == "__main__":
    num_listings = input("Enter number of listings to fetch (-1 to inf): ")
    location = input("Enter location to fetch listings from (Balcatta, 6021): ")
    fetch_type = input("Fetch available or sold listings (buy, sold): ")

    if num_listings is None or num_listings == 0:
        print("Entered listings amount is invalid")

    if location is None or location == "":
        print("Entered location is invalid")

    if fetch_type is None or fetch_type not in ["buy", "sold"]:
        print("Entered fetch type is invalid")

    listings = client.search(
        limit=int(num_listings), locations=[location], channel=fetch_type
    )

    run(listings=listings, location=location)
