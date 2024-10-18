import { Box, Typography } from "@mui/material";

const InfoBase = () => {
    const companyInfo = {
        maCongTy: "CT12345",
        nguoiDungDau: "Nguyễn Văn A",
        namThanhLap: 2020,
        nganhNghe: "Công nghệ thông tin",
        coCauCoDong: "Cổ đông lớn, Cổ đông nhỏ",
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
        </Box>
    );
};

export default InfoBase;
