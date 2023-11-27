import React from 'react';
import { CURR_YEAR } from '../../constants';

function Footer() {
  return (
    <footer className="body-font">
      <div className="bg-gray-100 border-t border-gray-300">
        <div className="container mx-auto py-4 px-5">
          <p className="text-gray-500 text-sm text-center">
            {`© ${CURR_YEAR} GitHub Trends`}
          </p>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
