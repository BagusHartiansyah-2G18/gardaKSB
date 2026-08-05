INSERT INTO master_desa (kecamatan_id, kode, nama) VALUES
(1,'BEL','Belo'),
(1,'BER','Beru'),
(1,'DSA','Dasan Anyar'),
(1,'GOA','Goa'),

(2,'BNJ','Banjar'),
(2,'BTP','Batu Putih'),
(2,'LBL','Labuhan Liang'),
(2,'LBR','Labuhan Lalar'),
(2,'LBK','Labuhan Kertasari'),
(2,'SRM','Sermong'),
(2,'SLT','Seloto'),
(2,'TMK','Tamekan'),
(2,'ARK','Arab Kenangan'),
(2,'BUG','Bugis'),
(2,'DLM','Dalam'),
(2,'KUA','Kuang'),
(2,'MNL','Menala'),
(2,'SMP','Sampir'),
(2,'TLB','Telaga Bertong'),

(3,'ARS','Air Suning'),
(3,'DSL','Desaloka'),
(3,'KLN','Kelanir'),
(3,'LMS','Lamusung'),
(3,'MRR','Meraran'),
(3,'RMP','Rempe'),
(3,'SRN','Seran'),
(3,'STA','Seteluk Atas'),
(3,'STT','Seteluk Tengah'),
(3,'TPR','Tapir'),

(4,'AIK','Ai Kangkung'),
(4,'KMN','Kemuning'),
(4,'SKA','Sekongkang Atas'),
(4,'SKB','Sekongkang Bawah'),
(4,'TLN','Talonang'),
(4,'TTR','Tatar'),
(4,'TNG','Tongo'),

(5,'BKM','Bangkat Monteh'),
(5,'DBR','Desa Beru'),
(5,'LMT','Lamuntet'),
(5,'MTG','Moteng'),
(5,'RRG','Rarak Ronges'),
(5,'SPB','Sapugara Bree'),
(5,'SMS','Seminar Salit'),
(5,'TPS','Tepas'),
(5,'TSP','Tepas Sepakat'),

(6,'KNT','Kiantar'),
(6,'KKL','Kokarlian'),
(6,'MTR','Mantar'),
(6,'PTT','Poto Tano'),
(6,'SNY','Senayan'),
(6,'TBS','Tambak Sari'),
(6,'TBO','Tebo'),
(6,'TNA','Tuananga'),

(7,'KLM','Kalimantong'),
(7,'LPK','Lampok'),
(7,'MNM','Manemeng'),
(7,'MTY','Mataiyang'),
(7,'MJD','Mujahiddin'),
(7,'MRA','Mura'),

(8,'BNT','Benete'),
(8,'BKD','Bukit Damai'),
(8,'MLK','Maluk'),
(8,'MNT','Mantun'),
(8,'PSP','Pasir Putih');

INSERT INTO master_kecamatan (id, kode, nama) VALUES
(1, 'JRW', 'Jereweh'),
(2, 'TLW', 'Taliwang'),
(3, 'STL', 'Seteluk'),
(4, 'SKG', 'Sekongkang'),
(5, 'BRE', 'Brang Rea'),
(6, 'PTO', 'Poto Tano'),
(7, 'BREN', 'Brang Ene'),
(8, 'MLK', 'Maluk');



INSERT INTO master_dinas (kode, nama, alamat, telepon) VALUES
('KESBANGPOL', 'Badan Kesatuan Bangsa dan Politik Kabupaten Sumbawa Barat', '', '')

INSERT INTO master_bidang (dinas_id, kode, nama, deskripsi) VALUES
(
    1,
    'IWKB',
    'Bidang Ideologi, Wawasan Kebangsaan, dan Karakter Bangsa',
    'Bidang yang menangani pembinaan ideologi Pancasila, wawasan kebangsaan, bela negara, dan karakter bangsa'
),
(
    1,
    'PDNO',
    'Bidang Politik Dalam Negeri dan Organisasi Kemasyarakatan',
    'Bidang yang menangani pendidikan politik, partisipasi politik, serta pembinaan dan pengawasan organisasi kemasyarakatan'
),
(
    1,
    'KWN',
    'Bidang Kewaspadaan Nasional',
    'Bidang yang menangani deteksi dini, kewaspadaan nasional, penanganan konflik sosial, dan pencegahan narkoba'
);


INSERT INTO accounts_user
(
    password,
    last_login,
    is_superuser,
    username,
    first_name,
    last_name,
    email,
    is_staff,
    is_active,
    date_joined,
    role,
    nik,
    no_hp
)
VALUES

-- ADMIN
(
    'pbkdf2_sha256$600000$dummy$dummy',
    NULL,
    1,
    'admin',
    'System',
    'Administrator',
    'admin@gardaksb.go.id',
    1,
    1,
    CURRENT_TIMESTAMP,
    'ADMIN',
    '0000000000000001',
    '081200000001'
),

-- KABAN
(
    'pbkdf2_sha256$600000$dummy$dummy',
    NULL,
    0,
    'kaban',
    'Kepala',
    'Kesbangpol',
    'kaban@gardaksb.go.id',
    1,
    1,
    CURRENT_TIMESTAMP,
    'KABAN',
    '0000000000000002',
    '081200000002'
),

-- SEKBAN
(
    'pbkdf2_sha256$600000$dummy$dummy',
    NULL,
    0,
    'sekban',
    'Sekretaris',
    'Kesbangpol',
    'sekban@gardaksb.go.id',
    1,
    1,
    CURRENT_TIMESTAMP,
    'SEKBAN',
    '0000000000000003',
    '081200000003'
),

-- KABID
(
    'pbkdf2_sha256$600000$dummy$dummy',
    NULL,
    0,
    'kabid_iwkb',
    'Kabid',
    'IWKB',
    'kabid.iwkb@gardaksb.go.id',
    1,
    1,
    CURRENT_TIMESTAMP,
    'KABID',
    '0000000000000004',
    '081200000004'
),

(
    'pbkdf2_sha256$600000$dummy$dummy',
    NULL,
    0,
    'kabid_pdno',
    'Kabid',
    'PDNO',
    'kabid.pdno@gardaksb.go.id',
    1,
    1,
    CURRENT_TIMESTAMP,
    'KABID',
    '0000000000000005',
    '081200000005'
),

(
    'pbkdf2_sha256$600000$dummy$dummy',
    NULL,
    0,
    'kabid_kwn',
    'Kabid',
    'KWN',
    'kabid.kwn@gardaksb.go.id',
    1,
    1,
    CURRENT_TIMESTAMP,
    'KABID',
    '0000000000000006',
    '081200000006'
),

-- ANGGOTA
(
    'pbkdf2_sha256$600000$dummy$dummy',
    NULL,
    0,
    'anggota1',
    'Anggota',
    'Satu',
    'anggota1@gardaksb.go.id',
    1,
    1,
    CURRENT_TIMESTAMP,
    'ANGGOTA',
    '0000000000000007',
    '081200000007'
),

(
    'pbkdf2_sha256$600000$dummy$dummy',
    NULL,
    0,
    'anggota2',
    'Anggota',
    'Dua',
    'anggota2@gardaksb.go.id',
    1,
    1,
    CURRENT_TIMESTAMP,
    'ANGGOTA',
    '0000000000000008',
    '081200000008'
),

(
    'pbkdf2_sha256$600000$dummy$dummy',
    NULL,
    0,
    'anggota3',
    'Anggota',
    'Tiga',
    'anggota3@gardaksb.go.id',
    1,
    1,
    CURRENT_TIMESTAMP,
    'ANGGOTA',
    '0000000000000009',
    '081200000009'
),

-- MASYARAKAT
(
    'pbkdf2_sha256$600000$dummy$dummy',
    NULL,
    0,
    'masyarakat1',
    'Budi',
    'Santoso',
    'masyarakat1@mail.com',
    0,
    1,
    CURRENT_TIMESTAMP,
    'MASYARAKAT',
    '5207010101010001',
    '081234567801'
),

(
    'pbkdf2_sha256$600000$dummy$dummy',
    NULL,
    0,
    'masyarakat2',
    'Siti',
    'Aminah',
    'masyarakat2@mail.com',
    0,
    1,
    CURRENT_TIMESTAMP,
    'MASYARAKAT',
    '5207010101010002',
    '081234567802'
),

(
    'pbkdf2_sha256$600000$dummy$dummy',
    NULL,
    0,
    'masyarakat3',
    'Ahmad',
    'Fauzi',
    'masyarakat3@mail.com',
    0,
    1,
    CURRENT_TIMESTAMP,
    'MASYARAKAT',
    '5207010101010003',
    '081234567803'
);


INSERT INTO auth_group (name) VALUES
('ADMIN'),
('KABAN'),
('SEKBAN'),
('KABID'),
('ANGGOTA'),
('MASYARAKAT');

INSERT INTO accounts_user_groups (user_id, group_id)
VALUES
(1, 1), -- admin -> ADMIN
(2, 2), -- kaban -> KABAN
(3, 3), -- sekban -> SEKBAN
(4, 4), -- kabid_iwkb -> KABID
(5, 4), -- kabid_pdno -> KABID
(6, 4), -- kabid_kwn -> KABID
(7, 5), -- anggota1 -> ANGGOTA
(8, 5), -- anggota2 -> ANGGOTA
(9, 5), -- anggota3 -> ANGGOTA
(10, 6), -- masyarakat1 -> MASYARAKAT
(11, 6), -- masyarakat2 -> MASYARAKAT
(12, 6); -- masyarakat3 -> MASYARAKAT

INSERT INTO pengaduan_pengaduan
(
    nomor_tiket,
    nama_pelapor,
    hp_pelapor,
    email_pelapor,
    alamat_pelapor,
    lokasi_kejadian,
    latitude,
    longitude,
    waktu_kejadian,
    uraian,
    pihak_terlibat,
    dampak,
    prioritas,
    anonim,
    source,
    status,
    verifikasi_admin,
    kesimpulan,
    ip_address,
    user_agent,
    created_at,
    updated_at,
    desa_id,
    jenis_kasus_id,
    pelapor_id
)
VALUES

(
    'KSB-202607-0001',
    'Budi Santoso',
    '081234567801',
    'masyarakat1@mail.com',
    'Desa Maluk, Kecamatan Maluk',
    'Area sekitar Pelabuhan Benete',
    -8.900000,
    116.740000,
    '2026-07-20 09:00:00',
    'Dugaan penyalahgunaan narkoba oleh sekelompok pemuda.',
    'Sekelompok pemuda',
    'Menimbulkan keresahan masyarakat sekitar.',
    'TINGGI',
    0,
    'WEB',
    'BARU',
    0,
    '',
    '127.0.0.1',
    'Mozilla/5.0',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP,
    64,
    1,
    10
),

(
    'KSB-202607-0002',
    'Siti Aminah',
    '081234567802',
    'masyarakat2@mail.com',
    'Kelurahan Menala, Kecamatan Taliwang',
    'Lapangan umum Taliwang',
    -8.739000,
    116.845000,
    '2026-07-21 14:30:00',
    'Terjadi ketegangan antar kelompok pemuda yang berpotensi konflik sosial.',
    'Dua kelompok pemuda',
    'Potensi gangguan keamanan dan ketertiban masyarakat.',
    'SEDANG',
    0,
    'WEB',
    'VERIFIKASI',
    1,
    'Memerlukan verifikasi lapangan.',
    '127.0.0.1',
    'Mozilla/5.0',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP,
    15,
    2,
    11
),

(
    'KSB-202607-0003',
    'Ahmad Fauzi',
    '081234567803',
    'masyarakat3@mail.com',
    'Desa Seteluk Tengah, Kecamatan Seteluk',
    'Balai Desa Seteluk Tengah',
    -8.685000,
    116.820000,
    '2026-07-22 10:15:00',
    'Dugaan kegiatan organisasi kemasyarakatan yang belum memiliki legalitas.',
    'Pengurus organisasi',
    'Potensi pelanggaran administrasi organisasi kemasyarakatan.',
    'RENDAH',
    0,
    'WEB',
    'PROSES',
    1,
    'Sedang dilakukan klarifikasi kepada pengurus organisasi.',
    '127.0.0.1',
    'Mozilla/5.0',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP,
    24,
    3,
    12
);


SELECT sql
FROM sqlite_master
WHERE name = 'pengaduan_verifikasipengaduan';

INSERT INTO pengaduan_verifikasipengaduan
(
    peran,
    status_verifikasi,
    catatan,
    tanggal_verifikasi,
    pengaduan_id,
    user_id
)
VALUES

(
    'ADMIN',
    1,
    'Laporan valid dan dapat diproses.',
    CURRENT_TIMESTAMP,
    1,
    1
),

(
    'ANGGOTA',
    1,
    'Hasil pengecekan lapangan menunjukkan indikasi benar.',
    CURRENT_TIMESTAMP,
    1,
    7
),

(
    'ADMIN',
    1,
    'Laporan diteruskan untuk verifikasi lapangan.',
    CURRENT_TIMESTAMP,
    2,
    1
),

(
    'ANGGOTA',
    1,
    'Ditemukan potensi konflik sosial, perlu monitoring.',
    CURRENT_TIMESTAMP,
    2,
    8
),

(
    'ADMIN',
    1,
    'Dokumen organisasi sedang diverifikasi.',
    CURRENT_TIMESTAMP,
    3,
    1
);


INSERT INTO pengaduan_pengaduanhistory
(
    judul,
    deskripsi,
    status_lama,
    status_baru,
    dokumentasi,
    latitude,
    longitude,
    created_at,
    pengaduan_id,
    user_id
)
VALUES

(
    'Laporan diterima',
    'Pengaduan berhasil diterima oleh sistem GARDA KSB.',
    'BARU',
    'VERIFIKASI',
    '',
    NULL,
    NULL,
    CURRENT_TIMESTAMP,
    1,
    1
),

(
    'Verifikasi lapangan',
    'Petugas melakukan verifikasi awal di lokasi kejadian.',
    'VERIFIKASI',
    'DISPOSISI',
    '',
    -8.900000,
    116.740000,
    CURRENT_TIMESTAMP,
    1,
    7
),

(
    'Disposisi ke Bidang Kewaspadaan Nasional',
    'Laporan didisposisikan untuk tindak lanjut.',
    'DISPOSISI',
    'PROSES',
    '',
    NULL,
    NULL,
    CURRENT_TIMESTAMP,
    1,
    6
),

(
    'Monitoring konflik sosial',
    'Tim melakukan monitoring perkembangan situasi.',
    'VERIFIKASI',
    'MONITORING',
    '',
    -8.739000,
    116.845000,
    CURRENT_TIMESTAMP,
    2,
    8
),

(
    'Klarifikasi organisasi',
    'Dilakukan klarifikasi kepada pengurus organisasi.',
    'PROSES',
    'SELESAI',
    '',
    -8.685000,
    116.820000,
    CURRENT_TIMESTAMP,
    3,
    5
);
INSERT INTO aktivitas_aktivitaspegawai
(
    judul,
    deskripsi,
    latitude,
    longitude,
    foto,
    tanggal_aktivitas,
    user_id
)
VALUES

(
    'Monitoring Wilayah Rawan Narkoba',
    'Monitoring lapangan terkait laporan dugaan penyalahgunaan narkoba.',
    -8.900000,
    116.740000,
    '',
    '2026-07-21 09:00:00',
    7
),

(
    'Verifikasi Konflik Sosial',
    'Verifikasi dugaan konflik sosial antar kelompok pemuda.',
    -8.739000,
    116.845000,
    '',
    '2026-07-22 10:30:00',
    8
),

(
    'Klarifikasi Organisasi Kemasyarakatan',
    'Klarifikasi administrasi organisasi masyarakat yang dilaporkan.',
    -8.685000,
    116.820000,
    '',
    '2026-07-23 13:00:00',
    9
),

(
    'Rapat Koordinasi IWKB',
    'Rapat koordinasi program wawasan kebangsaan.',
    -8.742000,
    116.838000,
    '',
    '2026-07-24 08:00:00',
    4
),

(
    'Pembinaan Organisasi Kemasyarakatan',
    'Kegiatan pembinaan terhadap organisasi masyarakat.',
    -8.745000,
    116.840000,
    '',
    '2026-07-24 14:00:00',
    5
),

(
    'Deteksi Dini Kewaspadaan Nasional',
    'Pemantauan wilayah dalam rangka deteksi dini gangguan keamanan.',
    -8.752000,
    116.835000,
    '',
    '2026-07-25 09:15:00',
    6
),

(
    'Monitoring Desa Binaan',
    'Kunjungan ke desa binaan untuk pengumpulan informasi lapangan.',
    -8.760000,
    116.830000,
    '',
    '2026-07-25 15:00:00',
    7
),

(
    'Sosialisasi Bahaya Narkoba',
    'Penyuluhan kepada masyarakat terkait pencegahan narkoba.',
    -8.748000,
    116.842000,
    '',
    '2026-07-26 08:30:00',
    8
);



INSERT INTO pengaduan_jeniskasus (id, kode, nama,warna)
VALUES
(1, 'NARKOBA', 'Penyalahgunaan Narkoba','rgba(250, 57, 36, 0.13)'),
(2, 'KONFLIK', 'Konflik Sosial','rgba(255, 25, 0, 0.13)'),
(3, 'ORMAS', 'Organisasi Kemasyarakatan','rgba(19, 204, 139, 0.13)');


INSERT INTO organisasi_jenisorganisasi
(
    kode,
    nama,
    deskripsi,
    is_active,
    created_at,
    updated_at
)
VALUES
(
    'ORMAS',
    'Organisasi Kemasyarakatan',
    'Organisasi kemasyarakatan yang terdaftar pada Kesbangpol',
    1,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
),
(
    'LSM',
    'Lembaga Swadaya Masyarakat',
    'Lembaga independen yang bergerak di bidang sosial dan kemasyarakatan',
    1,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
),
(
    'YAYASAN',
    'Yayasan',
    'Badan hukum yayasan yang bergerak di bidang sosial, pendidikan dan kemanusiaan',
    1,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
),
(
    'PAGUYUBAN',
    'Paguyuban',
    'Kelompok masyarakat dengan kesamaan latar belakang atau tujuan',
    1,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
),
(
    'KEPEMUDAAN',
    'Organisasi Kepemudaan',
    'Organisasi yang beranggotakan pemuda dan bergerak dalam kegiatan sosial kemasyarakatan',
    1,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

INSERT INTO organisasi_persyaratanorganisasi
(
    jenis_organisasi_id,
    nama,
    wajib
)
VALUES

-- ORMAS
(1, 'Surat Permohonan', 1),
(1, 'AD/ART', 1),
(1, 'SK Kepengurusan', 1),
(1, 'KTP Ketua', 1),
(1, 'KTP Sekretaris', 1),
(1, 'KTP Bendahara', 1),
(1, 'Surat Keterangan Domisili', 1),

-- LSM
(2, 'Akta Notaris', 1),
(2, 'SK Kemenkumham', 1),
(2, 'NPWP Lembaga', 1),
(2, 'Program Kerja', 1),

-- Yayasan
(3, 'Akta Pendirian Yayasan', 1),
(3, 'SK Kemenkumham', 1),
(3, 'NPWP Yayasan', 1),
(3, 'Susunan Pengurus', 1),

-- Paguyuban
(4, 'Daftar Pengurus', 1),
(4, 'Daftar Anggota', 1),
(4, 'Surat Domisili', 1),

-- Organisasi Kepemudaan
(5, 'AD/ART', 1),
(5, 'SK Kepengurusan', 1),
(5, 'Program Kerja Tahunan', 1);

INSERT INTO organisasi_organisasi
(
    jenis_organisasi_id,
    nama_organisasi,
    ketua_id,
    desa_id,
    alamat,
    nomor_sk,
    tanggal_sk,
    tanggal_berdiri,
    no_hp,
    email,
    logo,
    latitude,
    longitude,
    status_verifikasi
)
VALUES
(
    1,
    'Forum Bela Negara KSB',
    11,
    15,
    'Taliwang',
    'SK-001/KSB/2024',
    '2024-01-15',
    '2024-01-10',
    '081234567801',
    'fbnksb@gmail.com',
    'organisasi/default.png',
    -8.743500,
    116.845000,
    1
);
INSERT INTO organisasi_anggotaorganisasi
(
    organisasi_id,
    nama,
    nik,
    jabatan,
    no_hp,
    alamat
)
VALUES

-- Forum Bela Negara KSB
(
    1,
    'Budi Santoso',
    '5207010101010001',
    'Ketua',
    '081234567801',
    'Taliwang'
),
(
    1,
    'Indra Saputra',
    '5207010101010002',
    'Sekretaris',
    '081234567802',
    'Taliwang'
),
(
    1,
    'Rahmat Hidayat',
    '5207010101010003',
    'Bendahara',
    '081234567803',
    'Taliwang'
),

-- Forum Generasi Berencana KSB
(
    2,
    'Siti Aminah',
    '5207010101010004',
    'Ketua',
    '081234567804',
    'Seteluk'
),
(
    2,
    'Dian Pratama',
    '5207010101010005',
    'Sekretaris',
    '081234567805',
    'Seteluk'
),

-- LSM Peduli Sosial KSB
(
    3,
    'Ahmad Fauzi',
    '5207010101010006',
    'Ketua',
    '081234567806',
    'Maluk'
),
(
    3,
    'Feri Kurniawan',
    '5207010101010007',
    'Anggota',
    '081234567807',
    'Maluk'
),

-- Yayasan Cahaya Sumbawa Barat
(
    4,
    'Maya Lestari',
    '5207010101010008',
    'Pembina',
    '081234567808',
    'Jereweh'
),
(
    4,
    'Eko Prasetyo',
    '5207010101010009',
    'Ketua Yayasan',
    '081234567809',
    'Jereweh'
),

-- Karang Taruna Maju Bersama
(
    5,
    'Rizky Pratama',
    '5207010101010010',
    'Ketua',
    '081234567810',
    'Brang Rea'
),
(
    5,
    'Andi Saputra',
    '5207010101010011',
    'Wakil Ketua',
    '081234567811',
    'Brang Rea'
);
INSERT INTO organisasi_dokumenorganisasi
(
    organisasi_id,
    persyaratan_id,
    file,
    status,
    catatan_verifikasi,
    verified_by_id,
    verified_at
)
VALUES

-- Forum Bela Negara KSB
(
    1,
    1,
    'organisasi/surat_permohonan_fbn.pdf',
    'DISETUJUI',
    '',
    1,
    CURRENT_TIMESTAMP
),

(
    1,
    2,
    'organisasi/adart_fbn.pdf',
    'DISETUJUI',
    '',
    1,
    CURRENT_TIMESTAMP
),

(
    1,
    3,
    'organisasi/sk_pengurus_fbn.pdf',
    'DISETUJUI',
    '',
    1,
    CURRENT_TIMESTAMP
),

-- Forum Generasi Berencana
(
    2,
    1,
    'organisasi/surat_permohonan_genre.pdf',
    'DISETUJUI',
    '',
    1,
    CURRENT_TIMESTAMP
),

(
    2,
    2,
    'organisasi/adart_genre.pdf',
    'MENUNGGU',
    '',
    NULL,
    NULL
),

-- LSM Peduli Sosial
(
    3,
    8,
    'organisasi/akta_notaris_lsm.pdf',
    'DISETUJUI',
    '',
    1,
    CURRENT_TIMESTAMP
),

(
    3,
    9,
    'organisasi/sk_kemenkumham_lsm.pdf',
    'DITOLAK',
    'Dokumen kurang lengkap.',
    1,
    CURRENT_TIMESTAMP
),

(
    3,
    10,
    'organisasi/npwp_lsm.pdf',
    'MENUNGGU',
    '',
    NULL,
    NULL
),

-- Yayasan
(
    4,
    12,
    'organisasi/akta_yayasan.pdf',
    'DISETUJUI',
    '',
    1,
    CURRENT_TIMESTAMP
),

(
    4,
    13,
    'organisasi/sk_kemenkumham_yayasan.pdf',
    'DISETUJUI',
    '',
    1,
    CURRENT_TIMESTAMP
),

-- Karang Taruna
(
    5,
    18,
    'organisasi/adart_karang_taruna.pdf',
    'MENUNGGU',
    '',
    NULL,
    NULL
);


INSERT INTO informasi_materiberita
(
    user_id,
    kategori,
    judul,
    slug,
    deskripsi,
    cover_image,
    is_public,
    status_publish,
    published_at
)
VALUES

(
    1,
    'BERITA',
    'Kesbangpol KSB Gelar Sosialisasi Bahaya Narkoba',
    'kesbangpol-ksb-gelar-sosialisasi-bahaya-narkoba',
    'Kegiatan sosialisasi bahaya narkoba kepada masyarakat dan pelajar di Kabupaten Sumbawa Barat.',
    'materi/sosialisasi_narkoba.jpg',
    1,
    1,
    CURRENT_TIMESTAMP
),

(
    1,
    'BERITA',
    'Forum Bela Negara KSB Resmi Terdaftar',
    'forum-bela-negara-ksb-resmi-terdaftar',
    'Forum Bela Negara Kabupaten Sumbawa Barat telah resmi terdaftar dan mendapatkan pembinaan dari Kesbangpol.',
    'materi/forum_bela_negara.jpg',
    1,
    1,
    CURRENT_TIMESTAMP
),

(
    3,
    'PENGUMUMAN',
    'Pendaftaran Organisasi Kemasyarakatan Tahun 2026',
    'pendaftaran-organisasi-kemasyarakatan-2026',
    'Kesbangpol Kabupaten Sumbawa Barat membuka pendaftaran dan pembaruan data organisasi kemasyarakatan.',
    'materi/ormas_2026.jpg',
    1,
    1,
    CURRENT_TIMESTAMP
),

(
    4,
    'ARTIKEL',
    'Pentingnya Wawasan Kebangsaan bagi Generasi Muda',
    'pentingnya-wawasan-kebangsaan-bagi-generasi-muda',
    'Artikel edukatif mengenai wawasan kebangsaan sebagai fondasi pembangunan karakter generasi muda.',
    'materi/wawasan_kebangsaan.jpg',
    1,
    1,
    CURRENT_TIMESTAMP
),

(
    5,
    'ARTIKEL',
    'Deteksi Dini Konflik Sosial di Tingkat Desa',
    'deteksi-dini-konflik-sosial-di-tingkat-desa',
    'Strategi deteksi dini konflik sosial untuk menjaga stabilitas keamanan dan ketertiban masyarakat.',
    'materi/konflik_sosial.jpg',
    1,
    1,
    CURRENT_TIMESTAMP
),

(
    1,
    'PENGUMUMAN',
    'Jadwal Pelayanan Kesbangpol Bulan Agustus',
    'jadwal-pelayanan-kesbangpol-bulan-agustus',
    'Informasi jadwal pelayanan administrasi dan konsultasi organisasi kemasyarakatan.',
    'materi/pelayanan.jpg',
    1,
    0,
    NULL
);


INSERT INTO informasi_notifikasi
(
    user_id,
    jenis,
    judul,
    pesan,
    url,
    status_baca,
    created_at
)
VALUES

(
    11,
    'PENGADUAN',
    'Pengaduan Berhasil Dikirim',
    'Pengaduan dengan nomor tiket KSB-202607-0001 berhasil diterima sistem.',
    '/admin/pengaduan/pengaduan/1/change/',
    0,
    CURRENT_TIMESTAMP
),

(
    11,
    'PENGADUAN',
    'Pengaduan Sedang Diverifikasi',
    'Pengaduan Anda sedang diverifikasi oleh petugas Kesbangpol.',
    '/admin/pengaduan/pengaduan/1/change/',
    0,
    CURRENT_TIMESTAMP
),

(
    12,
    'ORGANISASI',
    'Dokumen Organisasi Disetujui',
    'Dokumen AD/ART Forum Bela Negara KSB telah disetujui.',
    '/admin/organisasi/dokumenorganisasi/',
    0,
    CURRENT_TIMESTAMP
),

(
    13,
    'ORGANISASI',
    'Dokumen Organisasi Ditolak',
    'Dokumen SK Kepengurusan ditolak. Silakan unggah dokumen yang lebih jelas.',
    '/admin/organisasi/dokumenorganisasi/',
    0,
    CURRENT_TIMESTAMP
),

(
    1,
    'PENGADUAN',
    'Pengaduan Baru Masuk',
    'Terdapat pengaduan baru yang memerlukan verifikasi admin.',
    '/admin/pengaduan/pengaduan/',
    0,
    CURRENT_TIMESTAMP
),

(
    3,
    'PENGADUAN',
    'Pengaduan Menunggu Disposisi',
    'Pengaduan telah selesai diverifikasi dan menunggu disposisi pimpinan.',
    '/admin/pengaduan/pengaduan/',
    0,
    CURRENT_TIMESTAMP
),

(
    5,
    'ORGANISASI',
    'Pendaftaran Organisasi Baru',
    'Terdapat organisasi baru yang menunggu verifikasi.',
    '/admin/organisasi/organisasi/',
    0,
    CURRENT_TIMESTAMP
),

(
    1,
    'BERITA',
    'Materi Berita Dipublikasikan',
    'Artikel baru telah dipublikasikan dan dapat diakses publik.',
    '/admin/informasi/materiberita/',
    1,
    CURRENT_TIMESTAMP
),

(
    1,
    'SISTEM',
    'Backup Database Berhasil',
    'Proses backup database harian berhasil dijalankan.',
    '',
    1,
    CURRENT_TIMESTAMP
);


INSERT INTO informasi_materiberita
(
    user_id,
    kategori,
    judul,
    slug,
    deskripsi,
    cover_image,
    file_pdf,
    is_public,
    status_publish,
    published_at
)
VALUES

(
    1,
    'MATERI',
    'Bahaya Penyalahgunaan Narkotika',
    'bahaya-penyalahgunaan-narkotika',
    'Materi edukasi bahaya narkotika.',
    'materi/narkoba.webp',
    'materi/pdf/bahaya-penyalahgunaan-narkotika.pdf',
    1,
    1,
    CURRENT_TIMESTAMP
),

(
    1,
    'MATERI',
    'Wawasan Kebangsaan',
    'wawasan-kebangsaan',
    'Materi wawasan kebangsaan untuk masyarakat.',
    'materi/wawasan.webp',
    'materi/pdf/wawasan-kebangsaan.pdf',
    1,
    1,
    CURRENT_TIMESTAMP
),

(
    1,
    'MATERI',
    'Bela Negara',
    'bela-negara',
    'Materi bela negara untuk generasi muda.',
    'materi/belanegara.webp',
    'materi/pdf/bela-negara.pdf',
    1,
    1,
    CURRENT_TIMESTAMP
),

(
    1,
    'MATERI',
    'Deteksi Dini Konflik Sosial',
    'deteksi-dini-konflik-sosial',
    'Pedoman pencegahan konflik sosial.',
    'materi/konflik.webp',
    'materi/pdf/deteksi-dini-konflik-sosial.pdf',
    1,
    1,
    CURRENT_TIMESTAMP
),

(
    1,
    'MATERI',
    'Penguatan Organisasi Kemasyarakatan',
    'penguatan-organisasi-kemasyarakatan',
    'Panduan tata kelola organisasi.',
    'materi/ormas.webp',
    'materi/pdf/penguatan-organisasi-kemasyarakatan.pdf',
    1,
    1,
    CURRENT_TIMESTAMP
);