import { Box, Typography } from "@mui/material";

const InfoBase = ({ data }) => {
    if (!data) {
        return <Typography variant="body1">Không có dữ liệu.</Typography>;
    }

    // Kiểm tra nếu data không rỗng
    if (Object.keys(data).length === 0) {
        return <Typography variant="body1">Đang tải dữ liệu...</Typography>;
    }

    const companyInfo = {
        maCongTy: data.overview.short_name,
        nguoiDungDau: data.shareholders.share_holder[1], 
        namThanhLap: data.overview.established_year,
        nganhNghe: data.overview.industry,
        sanGiaodich: data.overview.exchange,
        coCauCoDong: data.shareholders.share_holder.join(", "),
        website: data.overview.website,
        rating: data.overview.stock_rating,
        soLuongCoPhieu: `${Math.round(data.overview.issue_share[0])} triệu`
    };

    return (
        <Box padding={2}>
            <Typography variant="h6" fontWeight="bold" sx={{ color: 'black', fontSize: '24px' }}>
                Thông tin công ty
            </Typography>
            <Typography variant="body1" fontWeight="bold" sx={{ color: 'black', fontSize: '18px' }}>
                Mã công ty: <span style={{ fontWeight: 'normal' }}>{companyInfo.maCongTy}</span>
            </Typography>
            <Typography variant="body1" fontWeight="bold" sx={{ color: 'black', fontSize: '18px' }}>
                Người đứng đầu: <span style={{ fontWeight: 'normal' }}>{companyInfo.nguoiDungDau}</span>
            </Typography>
            <Typography variant="body1" fontWeight="bold" sx={{ color: 'black', fontSize: '18px' }}>
                Thành lập năm: <span style={{ fontWeight: 'normal' }}>{companyInfo.namThanhLap}</span>
            </Typography>
            <Typography variant="body1" fontWeight="bold" sx={{ color: 'black', fontSize: '18px' }}>
                Ngành nghề, lĩnh vực: <span style={{ fontWeight: 'normal' }}>{companyInfo.nganhNghe}</span>
            </Typography>
            <Typography variant="body1" fontWeight="bold" sx={{ color: 'black', fontSize: '18px' }}>
                Cơ cấu cổ đông: <span style={{ fontWeight: 'normal' }}>{companyInfo.coCauCoDong}</span>
            </Typography>
            <Typography variant="body1" fontWeight="bold" sx={{ color: 'black', fontSize: '18px' }}>
                Sàn giao dịch: <span style={{ fontWeight: 'normal' }}>{companyInfo.sanGiaodich}</span>
            </Typography>
            <Typography variant="body1" fontWeight="bold" sx={{ color: 'black', fontSize: '18px' }}>
                Website: <span style={{ fontWeight: 'normal' }}>{companyInfo.website}</span>
            </Typography>
            <Typography variant="body1" fontWeight="bold" sx={{ color: 'black', fontSize: '18px' }}>
                Đánh giá: <span style={{ fontWeight: 'normal' }}>{companyInfo.rating}</span>
            </Typography>
            <Typography variant="body1" fontWeight="bold" sx={{ color: 'black', fontSize: '18px' }}>
                Tổng số cổ phiếu: <span style={{ fontWeight: 'normal' }}>{companyInfo.soLuongCoPhieu}</span>
            </Typography>
        </Box>
    );
};

export default InfoBase;
