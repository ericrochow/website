Title: NX-OS Licensing
Date: 2017-02-24 12:11
Category: Network
Tags: network, nx-os, licensing
Authors: Eric Rochow
Summary: NX-OS Licensing

# NX-OS Licensing

## Obtaining a License

### What You Need

- Claim certificate or PAK number
- Serial number of the chassis to which the license will be applied. This can be obtained by issuing the following command:

    show license host-id

### Fulfilment Process

- Log into the [licensing portal](http://www.cisco.com/go/license).
- Go to License Administration Portal / Product License Registration.
- Click Get New Licenses From a PAK or Token and enter the Product Authorization Key on the Claim Certificate.
- Click Fulfill Single PAK / Token.
- Check the box in the column Quantity Available.
- Enter the chassis' serial number in the Serial Number field.
- Click the Assign button.
- Click Next.
- Check the I agree with the Terms of the License box.
- Click Get License.
- The license will be emailed to the account to which the Cisco account is associated. The license will also be available for download on the confirmation page.

## Applying a License

- Unzip the downloaded file and SCP the .lic file into the bootflash. Make sure the correct license file has been uploaded as the serial number is hard-coded into the license file.
- Issue the command `install license bootflash:///[name_of_file].lic`.
- Verify the license installation with the command `show license`.

## License Grace Period

If a device is not yet licensed for a feature that needs to be enabled immediately, all features can be unlocked for 120 days by issuing the following command:

    license grace-period

It is important to note that this command can only be issued a single time per chassis (it is tracked in hardware). After that, evaluation licenses will need to be requested on a case-by-case basis.
