FROM node:13.12.0-alpine as build
WORKDIR /app
COPY . ./
RUN npm ci --silent
RUN npm install react-scripts@3.4.1 -g --silent
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]