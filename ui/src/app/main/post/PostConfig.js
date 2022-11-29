import React from 'react';

const Post = React.lazy(() => import('./Post'));

const PostConfig = {
  settings: {
    layout: {
      config: {},
    },
  },
  routes: [
    {
      path: 'post',
      element: <Post />,
    },
  ],
};

export default PostConfig;

