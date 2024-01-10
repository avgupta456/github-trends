import React from 'react';

function Footer() {
  return (
    <footer className="body-font">
      <div className="bg-gray-100 border-t border-gray-300">
        <div className="container mx-auto py-4 px-5">
          <p className="text-gray-500 text-sm text-center">
            {`© ${new Date().getFullYear()} GitHub Trends`}
          </p>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
