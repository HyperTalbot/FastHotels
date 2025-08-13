// нужно будет решить с загрузкой фоток

// /** @type {import('next').NextConfig} */
// const nextConfig = {
//   images: {
//     remotePatterns: [
//       {
//         protocol: "http",
//         hostname: "localhost",
//         port: "8000",
//         pathname: "/static/**",
//       },
//     ],
//   },
// };

const nextConfig = {
  images: {
    unoptimized: true,
  },
};

module.exports = nextConfig;