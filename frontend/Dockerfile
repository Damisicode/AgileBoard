# Build Step
FROM node:18.19-alpine3.19 as build

WORKDIR /app
COPY package.json ./
RUN npm install
COPY . ./

RUN npm run build

# Release Step
FROM nginx:1.21.5-alpine as release
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app /usr/share/nginx/html
EXPOSE 80

ENTRYPOINT ["nginx", "-g", "daemon off;"]