import { type NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
  try {
    const data = await request.json()

    // In a real implementation, this would call your Python ML model
    // For now, we'll simulate the prediction logic

    // Simple risk scoring based on key factors
    let riskScore = 0
    const riskFactors: string[] = []

    // Credit Score Analysis
    const creditScore = Number.parseInt(data.credit_score) || 0
    if (creditScore < 600) {
      riskScore += 30
      riskFactors.push("Low Credit Score")
    } else if (creditScore < 700) {
      riskScore += 15
      riskFactors.push("Fair Credit Score")
    }

    // Debt-to-Income Ratio
    const dtir = Number.parseFloat(data.dtir1) || 0
    if (dtir > 43) {
      riskScore += 25
      riskFactors.push("High Debt-to-Income Ratio")
    } else if (dtir > 36) {
      riskScore += 10
      riskFactors.push("Moderate Debt-to-Income Ratio")
    }

    // Loan-to-Value Ratio
    const ltv = Number.parseFloat(data.ltv) || 0
    if (ltv > 90) {
      riskScore += 20
      riskFactors.push("High Loan-to-Value Ratio")
    } else if (ltv > 80) {
      riskScore += 10
      riskFactors.push("Moderate Loan-to-Value Ratio")
    }

    // Income Analysis
    const income = Number.parseInt(data.income) || 0
    const loanAmount = Number.parseInt(data.loan_amount) || 0
    if (income > 0 && loanAmount > 0) {
      const incomeRatio = loanAmount / income
      if (incomeRatio > 5) {
        riskScore += 15
        riskFactors.push("High Loan-to-Income Ratio")
      }
    }

    // Credit Worthiness
    if (data.credit_worthiness === "Poor") {
      riskScore += 20
      riskFactors.push("Poor Credit Worthiness")
    } else if (data.credit_worthiness === "Fair") {
      riskScore += 10
      riskFactors.push("Fair Credit Worthiness")
    }

    // Determine prediction based on risk score
    let prediction: "approved" | "rejected" | "review"
    let confidence: number
    let recommendation: string

    if (riskScore <= 20) {
      prediction = "approved"
      confidence = 85 + Math.random() * 10
      recommendation = "Low risk application. Recommended for approval with standard terms."
    } else if (riskScore <= 50) {
      prediction = "review"
      confidence = 70 + Math.random() * 15
      recommendation = "Moderate risk application. Manual review recommended with possible adjusted terms."
    } else {
      prediction = "rejected"
      confidence = 75 + Math.random() * 15
      recommendation = "High risk application. Consider rejection or require additional collateral/co-signer."
    }

    // Add some randomness for demo purposes
    if (Math.random() < 0.1) {
      prediction = prediction === "approved" ? "review" : prediction === "rejected" ? "review" : "approved"
    }

    return NextResponse.json({
      prediction,
      confidence,
      risk_factors: riskFactors.length > 0 ? riskFactors : ["Standard Risk Profile"],
      recommendation,
    })
  } catch (error) {
    console.error("Prediction API error:", error)
    return NextResponse.json({ error: "Failed to process prediction" }, { status: 500 })
  }
}
