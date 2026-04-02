"""
utils/region.py
───────────────
Định tuyến vị trí → server khu vực.
"""

# Danh sách tỉnh/thành theo khu vực
NORTH_PROVINCES = [
    "Hà Nội", "Hải Phòng", "Hải Dương", "Hưng Yên", "Bắc Ninh",
    "Vĩnh Phúc", "Thái Nguyên", "Bắc Giang", "Quảng Ninh", "Lạng Sơn",
    "Cao Bằng", "Bắc Kạn", "Tuyên Quang", "Lào Cai", "Yên Bái",
    "Hòa Bình", "Sơn La", "Điện Biên", "Lai Châu", "Phú Thọ",
    "Nam Định", "Thái Bình", "Hà Nam", "Ninh Bình", "Thanh Hóa",
]

SOUTH_PROVINCES = [
    "TP. Hồ Chí Minh", "Bình Dương", "Đồng Nai", "Bà Rịa - Vũng Tàu",
    "Long An", "Tiền Giang", "Bến Tre", "Vĩnh Long", "Trà Vinh",
    "Đồng Tháp", "An Giang", "Kiên Giang", "Cần Thơ", "Hậu Giang",
    "Sóc Trăng", "Bạc Liêu", "Cà Mau", "Tây Ninh", "Bình Phước",
    "Bình Thuận", "Ninh Thuận", "Lâm Đồng", "Đắk Nông", "Đắk Lắk",
    "Gia Lai", "Kon Tum", "Khánh Hòa", "Phú Yên", "Bình Định",
    "Quảng Ngãi", "Quảng Nam", "Đà Nẵng",
]

ALL_PROVINCES = sorted(NORTH_PROVINCES + SOUTH_PROVINCES)


def get_region_from_province(province: str) -> str:
    """Trả về 'north' hoặc 'south' dựa trên tên tỉnh/thành."""
    if province in NORTH_PROVINCES:
        return "north"
    return "south"


REGION_LABELS = {
    "north": "Mien Bac (Ha Noi)",
    "south": "Mien Nam (TP.HCM)",
}

REGION_COLORS = {
    "north": "#3b82f6",
    "south": "#22c55e",
}

# Toạ độ GPS mẫu (lat, lon) cho một số thành phố
GPS_COORDS = {
    "TP. Hồ Chí Minh": (10.8231, 106.6297),
    "Hà Nội":          (21.0285, 105.8542),
    "Đà Nẵng":         (16.0544, 108.2022),
    "Cần Thơ":         (10.0452, 105.7469),
    "Hải Phòng":       (20.8449, 106.6881),
}


def get_region_from_coords(lat: float, lon: float) -> str:
    """
    Phân vùng theo vĩ độ:
    - Bắc vĩ tuyến 14° → Miền Bắc
    - Nam vĩ tuyến 14° → Miền Nam
    (đơn giản hoá cho demo)
    """
    return "north" if lat >= 14.0 else "south"
