package com.lcm.user_service.service;


import com.lcm.user_service.entity.User;

import java.util.List;


public interface UserService {
    List<User> getAllUsers();
    User getUserById(Long id);
    User updateUser(Long id, User updatedUser);
    void deleteUser(Long id);
    User getUserByEmail(String email);
    User createUser(User user);
    User authenticateUser(String email, String password);
}
