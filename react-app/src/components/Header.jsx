import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <header className="bg-blue-600 text-white p-4">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-2xl font-bold">Traffic Sign Recognition</Link>
        <nav>
          <ul className="flex space-x-6">
            <li>
              <Link to="/" className="hover:text-blue-200">Trang chủ</Link>
            </li>
            <li>
              <Link to="/detect" className="hover:text-blue-200">Phát hiện biển báo</Link>
            </li>
            <li>
              <Link to="/classify" className="hover:text-blue-200">Phân loại biển báo</Link>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;
