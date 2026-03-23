.PHONY: local install clean build stop

# 默认使用 Homebrew 安装的 Ruby 3.2
RUBY_PATH := /usr/local/opt/ruby@3.2/bin
PORT := 4000

# 安装依赖
install:
	@echo "Installing dependencies..."
	@export PATH="$(RUBY_PATH):$(PATH)" && bundle install
	@echo "Done!"

# 停止已有服务
stop:
	@echo "Checking for existing Jekyll server on port $(PORT)..."
	@-lsof -ti:$(PORT) | xargs kill -9 2>/dev/null && echo "Stopped existing server" || echo "No server running"

# 本地预览
local: stop
	@echo ""
	@echo "Starting Jekyll server..."
	@echo "================================"
	@echo "Blog will be available at:"
	@echo "  http://localhost:$(PORT)/blog/"
	@echo "================================"
	@echo "Press Ctrl+C to stop"
	@echo ""
	@export PATH="$(RUBY_PATH):$(PATH)" && export LANG=en_US.UTF-8 && export LC_ALL=en_US.UTF-8 && bundle exec jekyll serve --host 0.0.0.0 --port $(PORT)

# 构建站点
build:
	@echo "Building site..."
	@export PATH="$(RUBY_PATH):$(PATH)" && export LANG=en_US.UTF-8 && export LC_ALL=en_US.UTF-8 && bundle exec jekyll build
	@echo "Done! Site is in _site/"

# 清理
clean:
	@echo "Cleaning..."
	rm -rf _site .bundle vendor
	@echo "Done!"

# 帮助
help:
	@echo "Available commands:"
	@echo "  make install  - Install dependencies"
	@echo "  make local    - Start local server (http://localhost:4000/blog/)"
	@echo "  make stop     - Stop running server"
	@echo "  make build    - Build site to _site/"
	@echo "  make clean    - Clean generated files"
	@echo "  make help     - Show this help"
	@echo ""
	@echo "Custom port:"
	@echo "  make local PORT=3000"
