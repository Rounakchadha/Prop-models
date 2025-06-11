def analyze_investment_opportunity_enhanced(self, locality, budget, horizon, risk_tolerance, 
                                          down_payment_percent=20, interest_rate=8.5, maintenance_percent=2):
    """Enhanced investment analysis with realistic maintenance costs"""
    
    locality_stats = self.get_locality_stats(locality)
    if not locality_stats:
        return {"error": "Locality data not available"}
    
    # Convert budget from lakhs to actual amount
    property_price = budget * 100000
    
    # 1. LOAN CALCULATIONS
    down_payment = property_price * (down_payment_percent / 100)
    loan_amount = property_price - down_payment
    
    monthly_interest_rate = interest_rate / (12 * 100)
    total_months = horizon * 12
    
    if monthly_interest_rate > 0:
        emi = (loan_amount * monthly_interest_rate * (1 + monthly_interest_rate) ** total_months) / \
              ((1 + monthly_interest_rate) ** total_months - 1)
    else:
        emi = loan_amount / total_months
    
    # 2. RENTAL INCOME ESTIMATION
    base_rent = locality_stats['avg_rent']
    avg_property_price = locality_stats['avg_price'] * 100000
    price_ratio = property_price / avg_property_price if avg_property_price > 0 else 1
    rent_scaling_factor = min(max(price_ratio, 0.8), 1.3)
    estimated_monthly_rent = base_rent * rent_scaling_factor
    
    # 3. REALISTIC MAINTENANCE AND EXPENSES
    
    # A. Basic Maintenance (Much Lower - 0.5% annually)
    realistic_maintenance_percent = 0.5  # Fixed at 0.5% annually
    monthly_basic_maintenance = (property_price * realistic_maintenance_percent / 100) / 12
    
    # B. Property Tax (realistic estimate)
    annual_property_tax = property_price * 0.001  # 0.1% annually
    monthly_property_tax = annual_property_tax / 12
    
    # C. Insurance
    annual_insurance = property_price * 0.002  # 0.2% annually
    monthly_insurance = annual_insurance / 12
    
    # D. Society Maintenance (for apartments)
    estimated_area_sqft = property_price / locality_stats.get('avg_rate_sqft', 10000)
    monthly_society_maintenance = estimated_area_sqft * 3  # ₹3 per sqft average
    
    # E. Vacancy Allowance
    vacancy_rate = 0.08  # 8% vacancy (about 1 month per year)
    monthly_vacancy_cost = estimated_monthly_rent * vacancy_rate
    
    # Total Monthly Expenses
    total_monthly_expenses = (
        monthly_basic_maintenance + 
        monthly_property_tax + 
        monthly_insurance + 
        monthly_society_maintenance + 
        monthly_vacancy_cost
    )
    
    # 4. CASH FLOW ANALYSIS
    monthly_cash_flow = estimated_monthly_rent - emi - total_monthly_expenses
    annual_cash_flow = monthly_cash_flow * 12
    
    # 5. ROI CALCULATIONS
    annual_rent = estimated_monthly_rent * 12
    annual_expenses = total_monthly_expenses * 12
    net_annual_income = annual_rent - annual_expenses
    
    # ROI on cash invested (down payment)
    roi_on_cash_invested = (net_annual_income / down_payment) * 100
    
    # 6. BREAK-EVEN ANALYSIS
    if net_annual_income > 0:
        break_even_years = down_payment / net_annual_income
    else:
        break_even_years = None
    
    # 7. RISK CALCULATION
    risk_score = self.calculate_realistic_risk_score(
        locality_stats, monthly_cash_flow, roi_on_cash_invested, risk_tolerance, property_price
    )
    
    # 8. TOTAL INTEREST CALCULATION
    total_emi_payments = emi * total_months
    total_interest_paid = total_emi_payments - loan_amount
    
    return {
        'locality': locality.title(),
        'budget': budget,
        'horizon': horizon,
        'property_price': round(property_price / 100000, 2),
        
        # Loan Details
        'down_payment': round(down_payment / 100000, 2),
        'loan_amount': round(loan_amount / 100000, 2),
        'monthly_emi': round(emi, 2),
        'total_interest': round(total_interest_paid / 100000, 2),
        'interest_rate': interest_rate,
        'down_payment_percent': down_payment_percent,
        
        # Rental Income
        'estimated_monthly_rent': round(estimated_monthly_rent, 2),
        'annual_rent_income': round(annual_rent, 2),
        
        # Expenses
        'monthly_maintenance': round(total_monthly_expenses, 2),  # Total expenses for compatibility
        'total_monthly_expenses': round(total_monthly_expenses, 2),
        
        # Cash Flow
        'monthly_cash_flow': round(monthly_cash_flow, 2),
        'annual_cash_flow': round(annual_cash_flow, 2),
        'net_annual_income': round(net_annual_income, 2),
        
        # Returns
        'annual_roi': round(roi_on_cash_invested, 2),
        'break_even_years': round(break_even_years, 2) if break_even_years else None,
        
        # Risk Assessment
        'risk_score': risk_score,
        'recommendation': self.get_realistic_investment_recommendation(
            roi_on_cash_invested, monthly_cash_flow, risk_score
        ),
        
        # Maintenance Breakdown (for template compatibility)
        'maintenance_breakdown': {
            'basic_maintenance': round(monthly_basic_maintenance, 2),
            'property_tax': round(monthly_property_tax, 2),
            'insurance': round(monthly_insurance, 2),
            'society_maintenance': round(monthly_society_maintenance, 2),
            'vacancy_allowance': round(monthly_vacancy_cost, 2)
        }
    }
