/* ────────────────────────────────
   DATA
──────────────────────────────── */
const rides = [
  {
    id: '1', code: 'GX-20240301-001',
    date: '04/03/2026', time: '08:32',
    pickup:  '121 Nguyễn Huệ, Quận 1, TP.HCM',
    dropoff: 'Sân bay Tân Sơn Nhất, Tân Bình, TP.HCM',
    distance: '8.4 km', duration: '25 phút',
    fare: 95000, status: 'completed',
    driver: 'Trần Minh Khoa',
    dAvatar: 'https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?w=80&h=80&fit=crop',
    dRating: 4.8, plate: '51G-245.88',
    vehicle: 'GoCar', pay: 'momo', uRating: 5
  },
  {
    id: '2', code: 'GX-20240228-047',
    date: '28/02/2026', time: '14:15',
    pickup:  'Landmark 81, Bình Thạnh, TP.HCM',
    dropoff: 'Phố đi bộ Nguyễn Huệ, Quận 1, TP.HCM',
    distance: '5.2 km', duration: '18 phút',
    fare: 52000, status: 'completed',
    driver: 'Lê Văn Hùng',
    dAvatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=80&h=80&fit=crop',
    dRating: 4.6, plate: '51K-889.12',
    vehicle: 'GoBike', pay: 'cash', uRating: 4
  },
  {
    id: '3', code: 'GX-20240225-012',
    date: '25/02/2026', time: '19:44',
    pickup:  'Aeon Mall Tân Phú, TP.HCM',
    dropoff: 'Vincom Center, Quận 3, TP.HCM',
    distance: '6.1 km', duration: '22 phút',
    fare: 68000, status: 'cancelled',
    driver: 'Phạm Thị Lan',
    dAvatar: 'https://images.unsplash.com/photo-1531123897727-8f129e1688ce?w=80&h=80&fit=crop',
    dRating: 4.9, plate: '51F-123.45',
    vehicle: 'GoCar', pay: 'card',
    cancelReason: 'Tài xế không đến đúng điểm đón'
  },
  {
    id: '4', code: 'GX-20240222-089',
    date: '22/02/2026', time: '07:05',
    pickup:  'KDC Him Lam, Quận 7, TP.HCM',
    dropoff: 'Tòa nhà Bitexco, Quận 1, TP.HCM',
    distance: '12.3 km', duration: '38 phút',
    fare: 145000, status: 'completed',
    driver: 'Nguyễn Văn Bình',
    dAvatar: 'https://images.unsplash.com/photo-1607990281513-2c110a25bd8c?w=80&h=80&fit=crop',
    dRating: 4.7, plate: '51A-456.78',
    vehicle: 'GoCar', pay: 'zalopay', uRating: 5
  },
  {
    id: '5', code: 'GX-20240220-055',
    date: '20/02/2026', time: '11:20',
    pickup:  'Đại học Bách Khoa TP.HCM, Quận 10',
    dropoff: 'Chợ Bến Thành, Quận 1, TP.HCM',
    distance: '3.5 km', duration: '14 phút',
    fare: 38000, status: 'completed',
    driver: 'Hoàng Đức Tài',
    dAvatar: 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=80&h=80&fit=crop',
    dRating: 4.5, plate: '51B-678.90',
    vehicle: 'GoBike', pay: 'momo', uRating: 4
  },
  {
    id: '6', code: 'GX-20240218-031',
    date: '18/02/2026', time: '22:10',
    pickup:  'Bar 23, Bùi Viện, Quận 1, TP.HCM',
    dropoff: 'Sunrise City, Quận 7, TP.HCM',
    distance: '7.8 km', duration: '30 phút',
    fare: 89000, status: 'completed',
    driver: 'Vũ Thành Nam',
    dAvatar: 'https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=80&h=80&fit=crop',
    dRating: 4.8, plate: '51D-321.54',
    vehicle: 'GoCar', pay: 'cash', uRating: 5
  },
  {
    id: '7', code: 'GX-20240215-076',
    date: '15/02/2026', time: '09:00',
    pickup:  'Ga Sài Gòn, Quận 3, TP.HCM',
    dropoff: 'Bến xe Miền Đông, Bình Thạnh, TP.HCM',
    distance: '4.6 km', duration: '20 phút',
    fare: 55000, status: 'cancelled',
    driver: 'Đỗ Quang Vinh',
    dAvatar: 'https://images.unsplash.com/photo-1545167622-3a6ac756afa4?w=80&h=80&fit=crop',
    dRating: 4.3, plate: '51H-765.43',
    vehicle: 'GoCar', pay: 'cash',
    cancelReason: 'Khách hàng huỷ chuyến'
  },
  {
    id: '8', code: 'GX-20240210-019',
    date: '10/02/2026', time: '16:45',
    pickup:  'Lotte Mart Quận 7, TP.HCM',
    dropoff: 'Crescent Mall, Phú Mỹ Hưng, TP.HCM',
    distance: '2.1 km', duration: '10 phút',
    fare: 28000, status: 'completed',
    driver: 'Bùi Tiến Dũng',
    dAvatar: 'https://images.unsplash.com/photo-1552058544-f2b08422138a?w=80&h=80&fit=crop',
    dRating: 4.9, plate: '51E-111.22',
    vehicle: 'GoBike', pay: 'zalopay', uRating: 5
  },
  {
    id: '9', code: 'GX-20240206-041',
    date: '06/02/2026', time: '13:30',
    pickup:  'Bệnh viện Chợ Rẫy, Quận 5, TP.HCM',
    dropoff: 'Nhà thờ Đức Bà, Quận 1, TP.HCM',
    distance: '3.9 km', duration: '16 phút',
    fare: 44000, status: 'completed',
    driver: 'Phan Thị Thu',
    dAvatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=80&h=80&fit=crop',
    dRating: 4.7, plate: '51C-999.88',
    vehicle: 'GoCar', pay: 'momo', uRating: 4
  },
  {
    id: '10', code: 'GX-20240201-063',
    date: '01/02/2026', time: '18:00',
    pickup:  'Đảo Kim Cương, Quận 2, TP.HCM',
    dropoff: 'Trung tâm thương mại Estella Place, Quận 2',
    distance: '1.8 km', duration: '8 phút',
    fare: 22000, status: 'ongoing',
    driver: 'Lý Minh Tú',
    dAvatar: 'https://images.unsplash.com/photo-1603415526960-f7e0328c63b1?w=80&h=80&fit=crop',
    dRating: 4.6, plate: '51P-444.55',
    vehicle: 'GoBike', pay: 'card'
  }
];
