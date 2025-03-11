#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/string.hpp>
#include <serial/serial.h>
#include <chrono>
#include <thread>

class SerialBridge : public rclcpp::Node {
public:
    SerialBridge() : Node("serial_bridge"), serial_port("/dev/ttyACM0"), baud_rate(115200), wheel_radius(0.075), wheel_separation(0.5), linear_x(0.5), angular_z(0.0) {
        connect_serial();
        
        rpm_publisher = this->create_publisher<std_msgs::msg::String>("/motor_rpm", 10);
        
        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(100),
            std::bind(&SerialBridge::read_serial, this)
        );
        
        send_velocity_as_rpm();
    }

private:
    std::string serial_port;
    int baud_rate;
    serial::Serial ser;
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr rpm_publisher;
    rclcpp::TimerBase::SharedPtr timer_;
    double wheel_radius;
    double wheel_separation;
    double linear_x;
    double angular_z;

    void connect_serial() {
        while (true) {
            try {
                ser.setPort(serial_port);
                ser.setBaudrate(baud_rate);
                ser.setTimeout(serial::Timeout::simpleTimeout(2000));
                ser.open();
                RCLCPP_INFO(this->get_logger(), "Connected to Teensy on %s", serial_port.c_str());
                std::this_thread::sleep_for(std::chrono::seconds(2));
                return;
            } catch (const serial::IOException &e) {
                RCLCPP_ERROR(this->get_logger(), "Teensy not found on %s, retrying...", serial_port.c_str());
                std::this_thread::sleep_for(std::chrono::seconds(2));
            }
        }
    }

    void send_velocity_as_rpm() {
        int left_rpm = 30, right_rpm = 30;
        std::string command = "JOINT_VELOCITIES " + std::to_string(left_rpm) + " " + std::to_string(right_rpm) + "\n";
        try {
            ser.write(command);
            RCLCPP_INFO(this->get_logger(), "Sent: %s", command.c_str());
        } catch (const serial::IOException &e) {
            RCLCPP_ERROR(this->get_logger(), "Failed to send RPM, attempting to reconnect...");
            reconnect_serial();
        }
    }

    void read_serial() {
        try {
            if (ser.isOpen() && ser.available()) {
                std::string response = ser.readline();
                response.erase(response.find_last_not_of(" \n\r") + 1); // Trim whitespace
                if (response.rfind("RPM", 0) == 0) { // Check if it starts with "RPM"
                    std_msgs::msg::String msg;
                    msg.data = response;
                    rpm_publisher->publish(msg);
                    RCLCPP_INFO(this->get_logger(), "Teensy: %s", response.c_str());
                }
            }
        } catch (const serial::IOException &e) {
            RCLCPP_ERROR(this->get_logger(), "Serial connection lost, attempting to reconnect...");
            reconnect_serial();
        }
    }

    void reconnect_serial() {
        RCLCPP_INFO(this->get_logger(), "Closing serial connection...");
        ser.close();
        std::this_thread::sleep_for(std::chrono::seconds(2));
        
        while (true) {
            try {
                RCLCPP_INFO(this->get_logger(), "Attempting to reconnect...");
                ser.setPort(serial_port);
                ser.setBaudrate(baud_rate);
                ser.setTimeout(serial::Timeout::simpleTimeout(2000));
                ser.open();
                RCLCPP_INFO(this->get_logger(), "Reconnected to Teensy on %s", serial_port.c_str());
                std::this_thread::sleep_for(std::chrono::seconds(2));
                send_velocity_as_rpm();
                RCLCPP_INFO(this->get_logger(), "Sent fresh SETPOINT after reconnecting");
                return;
            } catch (const serial::IOException &e) {
                RCLCPP_ERROR(this->get_logger(), "Reconnection failed, retrying in 2s...");
                std::this_thread::sleep_for(std::chrono::seconds(2));
            }
        }
    }
};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<SerialBridge>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
