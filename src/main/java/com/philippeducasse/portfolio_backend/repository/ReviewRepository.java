package com.philippeducasse.portfolio_backend.repository;


import com.philippeducasse.portfolio_backend.model.Review;
import org.springframework.data.jpa.repository.JpaRepository;

//extending JpaRepository gives access to save(), findAll(), etc.
public interface ReviewRepository extends JpaRepository<Review, Integer> {
}
