import os


# =====================================================
# SEARCH FILES
# =====================================================

def search_files(search_term):

    matches = []

    search_term = search_term.lower()

    # ==========================================
    # SEARCH LOCATIONS
    # ==========================================

    search_paths = [

        r"D:\Krish Things",

        os.path.expanduser("~/Documents"),

        os.path.expanduser("~/Desktop"),

        os.path.expanduser("~/Downloads")
    ]

    # ==========================================
    # WALK THROUGH FILES
    # ==========================================

    for base_path in search_paths:

        if not os.path.exists(base_path):
            continue

        for root, dirs, files in os.walk(base_path):

            for file in files:

                if search_term in file.lower():

                    full_path = os.path.join(
                        root,
                        file
                    )

                    matches.append(full_path)

                    # ==================================
                    # LIMIT RESULTS
                    # ==================================
                    if len(matches) >= 10:
                        return matches

    return matches