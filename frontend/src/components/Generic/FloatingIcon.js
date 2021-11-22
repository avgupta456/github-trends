import React from 'react';

import { FaGithub as GithubIcon } from 'react-icons/fa';

const FloatingIcon = () => {
  return (
    <div className="fixed bottom-8 right-8">
      <a
        href="https://www.github.com/avgupta456/github-trends"
        target="_blank"
        rel="noopener noreferrer"
      >
        <button
          type="button"
          className="rounded-sm shadow bg-gray-700 hover:bg-gray-800 text-gray-50 px-3 py-2 flex items-center"
        >
          Star on
          <GithubIcon className="ml-1.5 w-5 h-5" />
        </button>
      </a>
    </div>
  );
};

export default FloatingIcon;
