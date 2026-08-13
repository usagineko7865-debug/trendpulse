# Static production build served by nginx. Build & run:
#   docker build -t trendpulse-frontend --build-arg VITE_API_BASE_URL=https://your-api.example.com .
#   docker run -p 8080:80 trendpulse-frontend
#
# Deploys as-is on any static host too (Vercel/Netlify/Cloudflare Pages
# auto-detect Vite — just point them at this directory, no Dockerfile
# needed there). This Dockerfile exists for self-hosting on Railway/Fly/a VPS.
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
ARG VITE_API_BASE_URL
ARG VITE_STRIPE_PAYMENT_LINK
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}
ENV VITE_STRIPE_PAYMENT_LINK=${VITE_STRIPE_PAYMENT_LINK}
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
