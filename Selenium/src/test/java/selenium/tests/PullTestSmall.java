package selenium.tests;

import static org.junit.Assert.*;

import java.util.List;

import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.Keys;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.htmlunit.HtmlUnitDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import io.github.bonigarcia.wdm.ChromeDriverManager;


public class PullTestSmall {
	private static WebDriver driver;
	
	@BeforeClass
	public static void setUp() throws Exception 
	{
		//driver = new HtmlUnitDriver();
		ChromeDriverManager.getInstance().setup();
		driver = new ChromeDriver();
	}
	
	@AfterClass
	public static void  tearDown() throws Exception
	{
		driver.close();
		driver.quit();
	}
	
	@Test
	public void CreatePR() throws Exception
	{
		
	       driver.get("https://github.com/login");
	       WebElement id = driver.findElement(By.xpath("//input[@id='login_field']"));
	       WebElement pass = driver.findElement(By.xpath("//input[@id='password']"));
	       WebElement button = driver.findElement(By.xpath("//input[@value='Sign in']"));        

	       id.sendKeys("KakanotCollaborator");
	       pass.sendKeys("codekaka123");
	       button.submit();
	       WebDriverWait wait = new WebDriverWait(driver, 30);
	      // driver.get("https://github.com/codekaka/Repo1");
//	       WebElement pullReq = driver.findElement(By.xpath("//div[2]/div[1]/div[3]/div/div/div/a"));
//	       if(pullReq != null){
//	    	   pullReq.click();
//	    	   WebElement nxtScreenPullRequest = driver.findElement(By.xpath("//*[@id='new_pull_request']/div[2]/div/div/div[3]/button"));
//	    	   nxtScreenPullRequest.click();
//
//	    	   
//	       }
	       //change patch no
	       int i = 11;
	       String patchNo = "patch-11";
	       //end patch
	       driver.get("https://github.com/KakanotCollaborator/Repo1");

	       WebElement PR1 = driver.findElement(By.xpath("//div[2]/div[1]/div[4]/a"));

	       if(PR1 != null)
	       {

	    	   PR1.click();
	    	   driver.get("https://github.com/codekaka/Repo1/compare/master...KakanotCollaborator:master");
	    	   WebElement listBranches = driver.findElement(By.xpath("//div[2]/div[1]/div[1]/div[3]/div[2]/div[2]/button/span"));
	   		   listBranches.click();
	    	   wait.until(ExpectedConditions.visibilityOfElementLocated(By.xpath("//div[2]/div[1]/div[1]/div[3]/div[2]/div[2]/div/div/div[3]/div[1]/a["+i+"]/div")));
	    	   WebElement branchLatest = driver.findElement(By.xpath("//div[2]/div[1]/div[1]/div[3]/div[2]/div[2]/div/div/div[3]/div[1]/a["+i+"]/div"));

	    	   branchLatest.click();
	   		   driver.get("https://github.com/codekaka/Repo1/compare/master...KakanotCollaborator:KakanotCollaborator-"+patchNo);	
	    	   WebElement PR2 = driver.findElement(By.xpath("//div[2]/div[1]/div[2]/div/button"));
	    	   PR2.click();

	    	   WebElement PR3 = driver.findElement(By.xpath("//div[2]/div/div/div[3]/button"));
	    	   PR3.click();
	    	   WebElement commentFromKaka = driver.findElement(By.xpath("//div[2]/div/p"));
	    	   assertNotNull(commentFromKaka);
	       }
	}

}
