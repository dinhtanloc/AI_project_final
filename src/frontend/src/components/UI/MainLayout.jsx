import { Outlet } from 'react-router-dom';

const MainLayout = () => {
  return (
    <div style={{ backgroundColor: '#fff' }}>
      <Outlet />
    </div>
  );
};

export default MainLayout;
