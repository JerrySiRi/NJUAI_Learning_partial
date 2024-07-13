import glfw

def main():
    # 初始化库
    if not glfw.init():
        return
    # 创建窗口模及其OpenGL上下文
    window = glfw.create_window(640, 480, "Hello World", None, None)
    if not window:
        glfw.terminate()
        return
    # 将窗口设置为当前的上下文
    glfw.make_context_current(window)
    # 循环打开显示窗口，直到用户关闭窗口为止
    while not glfw.window_should_close(window):
        # 开始渲染，使用pyOpenGL交换的缓冲区
        glfw.swap_buffers(window)
        # 轮询和处理事件
        glfw.poll_events()
    glfw.terminate()

if __name__ == "__main__":
    main()